from langchain.tools import tool
from tavily import TavilyClient
from shared.config import settings

import requests

from datetime import datetime, timedelta, timezone

import asyncio
import aiohttp
import urllib

@tool
def search_tool(query: str):
    """Search the web for information."""
    tavily_client = TavilyClient(api_key=settings.TAVILY_API_KEY)
    return tavily_client.search(query=query, max_results=2)


@tool
async def calculate_tool(formula: str):
    """Calculate the result of a mathematical formula."""
    encoded_query=urllib.parse.quote(formula)
    url=f"https://api.wolframalpha.com/v2/query?input={encoded_query}&appid={settings.APP_ID}&output=json"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                response= await response.json() 
                return response['queryresult']['pods'][1]['subpods'][0]['plaintext']
            else:
                raise Exception(f"Error: {response.status}")
@tool
def is_now():
    """Datetime in VietNam"""
    vietnam_tz = timezone(timedelta(hours=7))
    current_time = datetime.now(vietnam_tz)
    return current_time.strftime("%Y-%m-%d %H:%M:%S GMT+7")

@tool
def get_weather(city:str):
    """Get weather infromation by city name"""
    if city.lower() == "hồ chí minh" or city.lower() == "ho chi minh" or city.lower() == "hcm":
        whether="Nắng ẩm mưa nhiều"
    elif city.lower()=="hà nội" or city.lower()=="ha noi" or city.lower()=="hn":
        whether="Mát mẻ"
    elif city.lower()=="đà nẵng" or city.lower()=="da nang":
        whether="Nắng và biển"
    else:
        whether="Không rõ"
    return whether



def format_search_result(result):
    lines=[]
    for i, item in enumerate(result['results'], start=1):
        lines.append(f"[{i}] {item['title']}")
        lines.append(f"   {item['url']}")
        lines.append(f"   {item['content']}")
        lines.append("-" * 50)
    return "\n".join(lines)

if __name__ == "__main__":
    query="Thông tin cơ bản về CR7"
    search_result=search_tool(query=query)
    result_type=type(search_result)
    
    print(format_search_result(search_result))

    print("================== CALCULATE ======================")
    result=asyncio.run(calculate_tool("2+3"))
    print(result)

    print("================== GET WEATHER ======================")
    result=get_weather("Hồ Chí Minh")
    print(result)
