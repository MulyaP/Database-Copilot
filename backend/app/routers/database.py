from fastapi import APIRouter, HTTPException
from ..models.database import DatabaseConnection, ConnectionResponse
from ..services.database_service import database_service

router = APIRouter(prefix="/api/database", tags=["database"])

@router.post("/connect", response_model=ConnectionResponse)
async def connect_database(connection: DatabaseConnection):
    """Connect to a database with provided credentials"""
    result = await database_service.connect_database(connection)
    
    if not result.success:
        raise HTTPException(status_code=400, detail=result.message)
    
    return result

@router.get("/status/{connection_id}")
async def check_connection_status(connection_id: str):
    """Check if a connection is still active"""
    if connection_id not in database_service.connections:
        raise HTTPException(status_code=404, detail="Connection not found")
    
    return {"status": "active", "connection_id": connection_id}

@router.delete("/disconnect/{connection_id}")
async def disconnect_database(connection_id: str):
    """Disconnect from a database"""
    if connection_id not in database_service.connections:
        raise HTTPException(status_code=404, detail="Connection not found")
    
    # Close the connection
    connection_info = database_service.connections[connection_id]
    try:
        if connection_info["provider"] in ["mysql", "postgresql"]:
            connection_info["connection"].close()
        elif connection_info["provider"] == "mongodb":
            connection_info["connection"].close()
    except:
        pass  # Connection might already be closed
    
    del database_service.connections[connection_id]
    return {"message": "Disconnected successfully"}

@router.get("/test")
async def test_connection():
    """Test endpoint to verify API is working"""
    return {"message": "Database API is working"}