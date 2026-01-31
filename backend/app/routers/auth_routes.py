from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from app.services.db_connect import get_supabase_client

router = APIRouter(prefix="/api", tags=["auth"])

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserSignup(BaseModel):
    name: str
    email: EmailStr
    password: str

@router.post("/login")
async def login(user_data: UserLogin):
    """
    Authenticate a user using Supabase Auth.
    """
    supabase = get_supabase_client()

    if not supabase:
        raise HTTPException(
            status_code=500, 
            detail="Failed to initialize Supabase client"
        )

    try:
        auth_response = supabase.auth.sign_in_with_password({
            "email": user_data.email,
            "password": user_data.password
        })

        if not auth_response.user or not auth_response.session:
             raise HTTPException(status_code=401, detail="Login failed")

        return {
            "message": "Login successful",
            "access_token": auth_response.session.access_token,
            "refresh_token": auth_response.session.refresh_token,
            "user": {
                "id": auth_response.user.id,
                "email": auth_response.user.email
            }
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/signup")
async def signup(user_data: UserSignup):
    """
    Register a new user using Supabase Auth and add to custom users table.
    """
    supabase = get_supabase_client()

    if not supabase:
        raise HTTPException(
            status_code=500, 
            detail="Failed to initialize Supabase client"
        )

    try:
        # Step 1: Sign up with Supabase Auth
        auth_response = supabase.auth.sign_up({
            "email": user_data.email, 
            "password": user_data.password
        })
        
        if not auth_response.user or not auth_response.user.id:
            # Check if there is an error in the response implied? 
            # supabase-py usually raises exception on error, but let's be safe.
             raise HTTPException(status_code=400, detail="Signup failed during auth step")

        user_id = auth_response.user.id

        # Step 2: Insert into custom users table
        # user_data is a reserved name in local scope, so using user_data.name
        
        custom_user_data = {
            "id": user_id,
            "name": user_data.name,
            "email": user_data.email
        }
        
        # Using the standard supabase client to insert
        data = supabase.table("users").insert(custom_user_data).execute()
        
        return {
            "message": "User registered successfully", 
            "user": {
                "id": user_id,
                "email": user_data.email,
                "name": user_data.name
            }
        }

    except Exception as e:
        # In a real app, we might want to clean up the auth user if table insert fails
        # But for now, just return the error
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/signout")
async def signout(tokens: dict):
    """
    Sign out the current user. 
    Requires access_token and refresh_token in the body to invalidate the session on Supabase.
    """
    supabase = get_supabase_client()
    if not supabase:
        raise HTTPException(status_code=500, detail="Supabase client initialization failed")

    access_token = tokens.get("access_token")
    refresh_token = tokens.get("refresh_token")

    if not access_token:
         # If no token, we can't really "sign out" on server, so just return success
         # as the frontend has likely cleared its part.
         return {"message": "Signed out successfully (no token provided)"}

    try:
        # To sign out a specific user from the server side using the python client,
        # we generally need to set the session for that client instance first.
        # Note: set_session might throw if tokens are invalid/expired.
        if refresh_token:
            supabase.auth.set_session(access_token, refresh_token)
        
        # Now sign out the user (invalidates the refresh token)
        supabase.auth.sign_out()
        
        return {"message": "Signed out successfully"}
    except Exception as e:
        # Even if it fails (e.g. token expired), we effectively want the user logged out.
        # So we can log the error but still return success or a specific code.
        print(f"Signout error: {e}")
        return {"message": "Signed out locally (server session invalidation failed or not needed)"}

