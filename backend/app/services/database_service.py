import uuid
from typing import Dict, Any
from ..models.database import DatabaseConnection, ConnectionResponse
from app.services.db_connect import get_supabase_client


# Optional imports for database drivers
try:
    import mysql.connector
except ImportError:
    mysql = None

try:
    import psycopg2
except ImportError:
    psycopg2 = None

try:
    import pymongo
except ImportError:
    pymongo = None

try:
    from supabase import create_client, Client
except ImportError:
    create_client = None

class DatabaseService:
    def __init__(self):
        self.active_connection: str|None = None 

    async def check_connection(self, connection_id: str) -> str:
        # if connection_id in self.connections:
        #     return True

        supabase = get_supabase_client()
        
        if not supabase:
            return ""
        
        result = supabase.table("connections").select("*").eq("id", connection_id).execute()
        
        if result.data:
            return result.data[0]['id']
        else:
            return ""
        
    async def get_connections(self, user_id: str) -> list[ConnectionResponse]:
        supabase = get_supabase_client()
        
        if not supabase:
            return []
        
        # Fetch connections for the user
        result = supabase.table("connections").select("*").eq("user_id", user_id).execute()
        
        if result.data:
            # self.connections = {
            #     str(conn['id']): {
            #         "provider": conn['db_provider'],
            #         "connection": conn['credentials']
            #     }
            #     for conn in result.data
            # }
            # return self.connections
            return (ConnectionResponse(
                success=True,
                message="Connections fetched successfully",
                connection_id=str(conn['id']),
                db_name=conn['db_name'],
                credentials=conn['credentials']
            ) for conn in result.data)
        else:
            return []
    
    async def create_connection(self, connection: DatabaseConnection) -> ConnectionResponse:
        try:
            # First, verify the connection actually works
            if connection.db_provider == "mysql":
                result = await self._connect_mysql(connection.credentials)
            elif connection.db_provider == "postgresql":
                result = await self._connect_postgresql(connection.credentials)
            elif connection.db_provider == "supabase":
                result = await self._connect_supabase(connection.credentials)
            elif connection.db_provider == "mongodb":
                result = await self._connect_mongodb(connection.credentials)
            else:
                return ConnectionResponse(success=False, message="Unsupported database provider")
            
            if result["success"]:
                supabase = get_supabase_client()
                if not supabase:
                    return ConnectionResponse(success=False, message="Failed to initialize backend Supabase client")

                connection_data = {
                    "user_id": connection.user_id,
                    "db_name": connection.db_name,
                    "db_provider_name": connection.db_provider,
                    "credentials": connection.credentials,
                    "connected": False
                }
                
                insert_result = supabase.table("connections").insert(connection_data).execute()
                
                if insert_result.data:
                    new_id = str(insert_result.data[0]['id'])
                    return await self.connect_database(new_id)
                else:
                    return ConnectionResponse(success=False, message="Failed to save connection to database")
            else:
                return ConnectionResponse(success=False, message=result["error"])
                
        except Exception as e:
            return ConnectionResponse(success=False, message=f"Connection failed: {str(e)}")
    
    async def connect_database(self, connection_id: str) -> ConnectionResponse:
        try:
            supabase = get_supabase_client()
            if not supabase:
                return ConnectionResponse(success=False, message="Failed to initialize backend Supabase client")
            
            # Get connection details
            result = supabase.table("connections").select("*").eq("id", connection_id).execute()
            if not result.data:
                return ConnectionResponse(success=False, message="Connection not found")
            
            conn_data = result.data[0]
            credentials = conn_data['credentials']
            db_provider = conn_data.get('db_provider_name', conn_data['db_name'])
            
            # Test the connection
            if db_provider == "mysql":
                test_result = await self._connect_mysql(credentials)
            elif db_provider == "postgresql":
                test_result = await self._connect_postgresql(credentials)
            elif db_provider == "supabase":
                test_result = await self._connect_supabase(credentials)
            elif db_provider == "mongodb":
                test_result = await self._connect_mongodb(credentials)
            else:
                return ConnectionResponse(success=False, message="Unsupported database provider")
            
            if test_result["success"]:
                # Update connected status and set active connection
                update_result = supabase.table("connections").update({"connected": True}).eq("id", connection_id).execute()
                
                if update_result.data:
                    self.active_connection = connection_id
                    return ConnectionResponse(success=True, message="Connected successfully", connection_id=connection_id)
                else:
                    return ConnectionResponse(success=False, message="Failed to update connection status")
            else:
                return ConnectionResponse(success=False, message=test_result["error"])
                
        except Exception as e:
            return ConnectionResponse(success=False, message=f"Connection failed: {str(e)}")
    
    async def disconnect_database(self):
        if not self.active_connection:
            return ConnectionResponse(success=False, message="No active connection to disconnect")
        
        supabase = get_supabase_client()
        if not supabase:
            return ConnectionResponse(success=False, message="Failed to initialize backend Supabase client")
        
        update_result = supabase.table("connections").update({"connected": False}).eq("id", self.active_connection).execute()
        
        if update_result.data:
            self.active_connection = None
            return ConnectionResponse(success=True, message="Disconnected successfully")
        else:
            return ConnectionResponse(success=False, message="Failed to disconnect from database")

    async def _connect_mysql(self, credentials: Dict[str, str]) -> Dict[str, Any]:
        if mysql is None:
            return {"success": False, "error": "MySQL driver not installed"}
            
        required_fields = ["host", "port", "username", "password", "database"]
        if not all(field in credentials for field in required_fields):
            return {"success": False, "error": "Missing required credentials"}
        
        try:
            connection = mysql.connector.connect(
                host=credentials["host"],
                port=int(credentials["port"]),
                user=credentials["username"],
                password=credentials["password"],
                database=credentials["database"]
            )
            connection.ping(reconnect=True)
            return {"success": True, "connection": connection}
        except Exception as e:
            return {"success": False, "error": f"MySQL connection failed: {str(e)}"}
    
    async def _connect_postgresql(self, credentials: Dict[str, str]) -> Dict[str, Any]:
        if psycopg2 is None:
            return {"success": False, "error": "PostgreSQL driver not installed"}
            
        required_fields = ["host", "port", "username", "password", "database"]
        if not all(field in credentials for field in required_fields):
            return {"success": False, "error": "Missing required credentials"}
        
        try:
            connection = psycopg2.connect(
                host=credentials["host"],
                port=int(credentials["port"]),
                user=credentials["username"],
                password=credentials["password"],
                database=credentials["database"]
            )
            cursor = connection.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
            return {"success": True, "connection": connection}
        except Exception as e:
            return {"success": False, "error": f"PostgreSQL connection failed: {str(e)}"}
    
    async def _connect_supabase(self, credentials: Dict[str, str]) -> Dict[str, Any]:
        if "connection_string" not in credentials:
            return {"success": False, "error": "Missing connection string"}
        
        try:
            from sqlalchemy import create_engine, text
            
            # Test connection with timeout and connection pool settings
            engine = create_engine(
                credentials["connection_string"],
                pool_timeout=30,
                pool_recycle=3600,
                connect_args={"connect_timeout": 30}
            )
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            
            return {"success": True, "connection": engine}
        except Exception as e:
            return {"success": False, "error": f"Supabase connection failed: {str(e)}"}
    
    async def _connect_mongodb(self, credentials: Dict[str, str]) -> Dict[str, Any]:
        if pymongo is None:
            return {"success": False, "error": "MongoDB driver not installed"}
            
        if "connection_string" not in credentials:
            return {"success": False, "error": "Missing connection string"}
        
        try:
            client = pymongo.MongoClient(credentials["connection_string"])
            # Test connection by pinging the server
            client.admin.command('ping')
            return {"success": True, "connection": client}
        except Exception as e:
            return {"success": False, "error": f"MongoDB connection failed: {str(e)}"}

database_service = DatabaseService()