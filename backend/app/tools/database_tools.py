
from typing import List, Dict, Any, Optional
from ..services.database_service import database_service
from ..services.db_connect import get_supabase_client
from supabase import create_client

class DatabaseTools:
    def _get_connection_data(self, connection_id: str):
        """Get connection data from database"""
        supabase = get_supabase_client()
        if not supabase:
            raise ValueError("Failed to initialize Supabase client")
        
        result = supabase.table("connections").select("*").eq("id", connection_id).execute()
        if not result.data:
            raise ValueError(f"Connection {connection_id} not found")
        
        return result.data[0]

    def list_tables(self, connection_id: str) -> List[str]:
        """
        List all tables in the connected database.
        """
        try:
            conn_data = self._get_connection_data(connection_id)
            db_provider = conn_data.get('db_provider_name', conn_data['db_name'])
            print(f"Debug: db_provider = {db_provider}")

            if db_provider == "supabase":
                query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
                print(f"Debug: Executing query: {query}")
                result = self.execute_sql_query(connection_id, query)
                print(f"Debug: Query result: {result}")
                
                if isinstance(result, list):
                    tables = [row.get('table_name') for row in result if 'table_name' in row]
                    print(f"Debug: Extracted tables: {tables}")
                    return tables
                elif isinstance(result, dict) and 'error' in result:
                    print(f"Debug: Error in query: {result['error']}")
                    return []
                return []
            
            print(f"Debug: Unsupported provider: {db_provider}")
            return []
        except Exception as e:
            print(f"Debug: Exception in list_tables: {str(e)}")
            return []

    def get_table_schema(self, connection_id: str, table_name: str) -> Dict[str, Any]:
        """
        Get the schema for a specific table.
        """
        query = f"""
            SELECT column_name, data_type, is_nullable 
            FROM information_schema.columns 
            WHERE table_schema = 'public' AND table_name = '{table_name}'
        """
        return self.execute_sql_query(connection_id, query)

    def execute_sql_query(self, connection_id: str, query: str) -> Any:
        """
        Execute a raw SQL query using SQLAlchemy.
        """
        conn_data = self._get_connection_data(connection_id)
        credentials = conn_data['credentials']
        db_provider = conn_data.get('db_provider_name', conn_data['db_name'])
        
        if db_provider == "supabase":
            try:
                from sqlalchemy import create_engine, text
                
                # Create engine with timeout settings
                engine = create_engine(
                    credentials["connection_string"],
                    pool_timeout=30,
                    pool_recycle=3600,
                    connect_args={"connect_timeout": 30}
                )
                with engine.connect() as connection:
                    result = connection.execute(text(query))
                    rows = result.fetchall()
                    
                    # Convert to list of dictionaries
                    columns = result.keys()
                    return [dict(zip(columns, row)) for row in rows]
                    
            except Exception as e:
                return {"error": f"Failed to execute SQL via SQLAlchemy: {str(e)}"}

        return {"error": "Unsupported provider"}

    def get_configured_tools(self, connection_id: str):
        """
        Returns a list of LangChain tools configured for the specific connection.
        """
        # from langchain.tools import StructuredTool # Deprecated/Moved
        from langchain_core.tools import StructuredTool
        from pydantic import BaseModel, Field

        # Define input models for tools (optional, but good for description)
        
        def list_tables_wrapper() -> str:
            """List all tables in the database."""
            return str(self.list_tables(connection_id))

        def get_schema_wrapper(table_name: str) -> str:
            """Get definition/schema of a specific table."""
            return str(self.get_table_schema(connection_id, table_name))

        def execute_sql_wrapper(query: str) -> str:
            """Execute a SQL query against the database. Use this to query data."""
            return str(self.execute_sql_query(connection_id, query))

        return [
            StructuredTool.from_function(
                func=list_tables_wrapper,
                name="list_tables",
                description="List all available tables in the database."
            ),
            StructuredTool.from_function(
                func=get_schema_wrapper,
                name="get_table_schema",
                description="Get the schema (columns, types) of a specific table."
            ),
            StructuredTool.from_function(
                func=execute_sql_wrapper,
                name="execute_sql_query",
                description="Execute a RAW SQL query to fetch data. Always verify table names with list_tables first."
            )
        ]

database_tools = DatabaseTools()
