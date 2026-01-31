from fastapi import APIRouter, HTTPException, Body, Header
from pydantic import BaseModel
from typing import List, Optional, Any
import os

from ..services.database_service import database_service
from ..tools.database_tools import database_tools
from ..services.db_connect import get_supabase_client

# LangChain Imports
# LangChain Imports
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
# from langchain.agents import AgentExecutor, create_tool_calling_agent # Deprecated/Removed
# from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_groq import ChatGroq
import json

router = APIRouter(prefix="/api/chat", tags=["chat"])

class ChatRequest(BaseModel):
    message: str
    connection_id: str
    model_provider: str = "groq" # "openai", "gemini", or "groq"

class ChatResponse(BaseModel):
    response: str
    tool_calls: List[Any] = []

@router.post("", response_model=ChatResponse)
async def query(request: ChatRequest, authorization: Optional[str] = Header(None)):
    # Verify user authentication
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid authorization header")
    
    access_token = authorization.split(" ")[1]
    
    try:
        supabase = get_supabase_client()
        if not supabase:
            raise HTTPException(status_code=500, detail="Failed to initialize Supabase client")
        
        # Verify access token
        user_response = supabase.auth.get_user(access_token)
        if not user_response.user:
            raise HTTPException(status_code=401, detail="Invalid access token")
            
    except Exception as e:
        raise HTTPException(status_code=401, detail="Authentication failed")
    # print(os.getenv("GROQ_API_KEY"))
    """
    Process a natural language query against the connected database.
    """
    # 1. Verify Connection - connection_id from frontend is source of truth
    # 2. Get Tools
    tools = database_tools.get_configured_tools(request.connection_id)
    
    # 3. Initialize LLM - Use OpenAI-compatible models with proper tool calling
    try:
        if os.getenv("GROQ_API_KEY"):
            llm = ChatGroq(model_name="llama-3.1-8b-instant", temperature=0)
           
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to initialize LLM: {str(e)}")

    # 4. Loop until no more tool calls
    try:
        llm_with_tools = llm.bind_tools(tools)
        messages = [HumanMessage(content=request.message)]
        all_tool_calls = []
        iteration = 0
        
        print(f"DEBUG: Starting chat loop for query: {request.message}")
        
        while True:
            iteration += 1
            print(f"DEBUG: Iteration {iteration} - Calling LLM")
            
            response = llm_with_tools.invoke(messages)
            
            if not response.tool_calls:
                print(f"DEBUG: No tool calls in response, returning final answer")
                print(f"DEBUG: Final response: {response.content[:100]}...")
                return ChatResponse(
                    response=response.content,
                    tool_calls=all_tool_calls
                )
            
            print(f"DEBUG: Found {len(response.tool_calls)} tool calls")
            
            # Execute tool calls
            messages.append(response)
            
            for i, tool_call in enumerate(response.tool_calls):
                tool_name = tool_call['name']
                tool_args = tool_call['args']
                
                print(f"DEBUG: Executing tool {i+1}/{len(response.tool_calls)}: {tool_name}({tool_args})")
                
                # Execute the tool
                if tool_name == 'list_tables':
                    result = database_tools.list_tables(request.connection_id)
                elif tool_name == 'get_table_schema':
                    result = database_tools.get_table_schema(request.connection_id, tool_args['table_name'])
                elif tool_name == 'execute_sql_query':
                    result = database_tools.execute_sql_query(request.connection_id, tool_args['query'])
                else:
                    result = f"Unknown tool: {tool_name}"
                
                print(f"DEBUG: Tool result: {str(result)[:200]}...")
                
                all_tool_calls.append({
                    'name': tool_name,
                    'args': tool_args,
                    'result': result
                })
                
                # Add tool result to conversation
                messages.append(ToolMessage(content=str(result), tool_call_id=tool_call['id']))
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Agent execution failed: {str(e)}")