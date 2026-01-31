from fastapi import APIRouter, HTTPException, Header
from ..models.database import DatabaseConnection, ConnectionResponse
from ..services.database_service import database_service
from ..services.db_connect import get_supabase_client
from typing import Optional

router = APIRouter(prefix="/api/database", tags=["database"])

@router.post("/create_connection", response_model=ConnectionResponse)
async def create_connection(connection: DatabaseConnection):
    if not connection.user_id:
        raise HTTPException(status_code=401, detail="User is not logged in!")
    """Connect to a database with provided credentials"""
    result = await database_service.create_connection(connection)
    
    if not result.success:
        raise HTTPException(status_code=400, detail=result.message)
    
    return result

@router.post("/connect/{connection_id}")
async def connect_database(connection_id: str):
    """Connect to a database with provided credentials"""
    result = await database_service.connect_database(connection_id)

    if not result.success:
        raise HTTPException(status_code=400, detail=result.message)

    return result

@router.get("/connections")
async def get_connections(authorization: Optional[str] = Header(None)):
    """Get all connections for the authenticated user"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid authorization header")
    
    access_token = authorization.split(" ")[1]
    
    try:
        supabase = get_supabase_client()
        if not supabase:
            raise HTTPException(status_code=500, detail="Failed to initialize Supabase client")
        
        # Get user from access token
        user_response = supabase.auth.get_user(access_token)
        if not user_response.user:
            raise HTTPException(status_code=401, detail="Invalid access token")
        
        user_id = user_response.user.id
        
        # Get connections for the user
        result = supabase.table("connections").select("*").eq("user_id", user_id).execute()
        
        return {"connections": result.data}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get connections: {str(e)}")

@router.get("/status/{connection_id}")
async def check_connection_status(connection_id: str):
    """Check if a connection is still active"""
    if not await database_service.check_connection(connection_id):
        raise HTTPException(status_code=404, detail="Connection not found")
    
    return {"status": "active", "connection_id": connection_id}

@router.post("/disconnect")
async def disconnect_database():
    """Disconnect from a database"""
    result = await database_service.disconnect_database()
    
    if not result.success:
        raise HTTPException(status_code=400, detail=result.message)
    
    return result