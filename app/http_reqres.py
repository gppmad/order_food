import asyncio
import json
import httpx

BASE_URL = 'nourish.me/api/v1'

async def get_menu():
    endpoint = f"{BASE_URL}/bulk/order"
    response = httpx.get(endpoint)
    
    return response


