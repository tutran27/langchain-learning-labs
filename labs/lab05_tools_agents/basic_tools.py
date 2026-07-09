from langchain.tools import tool
from tavily import TavilyClient
from shared.config import settings
import json

# Comment decorater lại do ko test tool được
@tool
def search_tool(query: str):
    """Search the web for information."""
    tavily_client = TavilyClient(api_key=settings.TAVILY_API_KEY)
    return tavily_client.search(query=query, max_results=2)

@tool
def add(a: float, b: float):
    """Add two numbers."""
    return a + b

@tool
def subtract(a: float, b: float):
    """Subtract two numbers."""
    return a - b

def format_print(data):
    print("==============================================")
    if isinstance(data, dict):
        print(json.dumps(data, indent=4, ensure_ascii=False))
    else:
        print(data)
    print("==============================================")

if __name__ == "__main__":
    query="Thông tin cơ bản về CR7"
    search_result=search_tool(query=query)
    result_type=type(search_result)
    
    format_print(result_type)
    format_print(search_result)
