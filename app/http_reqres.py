import httpx
import json
import os

BASE_URL = os.environ.get('BASE_URL') if os.environ.get('BASE_URL') else 'http://localhost:3000'


async def get_menu():
    endpoint = f"{BASE_URL}/menu"
    response = httpx.get(endpoint)
    return response


async def post_orders(employee_orders_list, menu):
    orders_json = []
    for el in employee_orders_list:
        if el.is_attending:
            orders_json.append(el.get_order(menu))
    endpoint = f"{BASE_URL}/bulk/order"
    headers = {'content-type':'application/json','accept':'application/json'}
    response = httpx.post(endpoint, json={'orders': orders_json}, headers=headers)
    return response
