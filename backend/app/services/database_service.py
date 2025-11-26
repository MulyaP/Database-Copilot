import uuid
from typing import Dict, Any
from ..models.database import DatabaseConnection, ConnectionResponse

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
        self.connections: Dict[str, Any] = {}
    
    async def connect_database(self, connection: DatabaseConnection) -> ConnectionResponse:
        try:
            connection_id = str(uuid.uuid4())
            
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
                self.connections[connection_id] = {
                    "connection": result["connection"],
                    "provider": connection.db_provider,
                    "type": connection.db_type
                }
                return ConnectionResponse(
                    success=True, 
                    message="Connected successfully", 
                    connection_id=connection_id
                )
            else:
                return ConnectionResponse(success=False, message=result["error"])
                
        except Exception as e:
            return ConnectionResponse(success=False, message=f"Connection failed: {str(e)}")
    
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
        if create_client is None:
            return {"success": False, "error": "Supabase driver not installed"}
            
        required_fields = ["supabase_url", "supabase_anon_key"]
        if not all(field in credentials for field in required_fields):
            return {"success": False, "error": "Missing required credentials"}
        
        try:
            supabase: Client = create_client(
                credentials["supabase_url"],
                credentials["supabase_anon_key"]
            )

            # Test connection by fetching user info
            users = (supabase.from_("users").select("id").execute())
            print(users.data)
            # response = supabase.auth.get_user()
            # print(response)
            # print(supabase)
            return {"success": True, "connection": supabase}
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