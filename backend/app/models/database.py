from pydantic import BaseModel
from typing import Dict, Literal

DatabaseType = Literal["sql", "nosql"]
DatabaseProvider = Literal["mysql", "postgresql", "supabase", "mongodb"]

class DatabaseConnection(BaseModel):
    user_id: str
    db_type: DatabaseType
    db_provider: DatabaseProvider
    db_name: str
    credentials: Dict[str, str]

class ConnectionResponse(BaseModel):
    success: bool
    message: str
    connection_id: str = None