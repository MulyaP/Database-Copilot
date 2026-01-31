import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_supabase_client() -> Client:
    """
    Creates and returns a Supabase client using environment variables.
    Returns None if credentials are missing.
    """
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_ANON_KEY")

    if not supabase_url or not supabase_key:
        print("Error: Supabase credentials not found in environment variables.")
        return None

    try:
        client = create_client(supabase_url, supabase_key)
        return client
    except Exception as e:
        print(f"Error connecting to Supabase: {e}")
        return None
