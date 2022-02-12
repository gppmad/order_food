import json
from typing import Optional
from fastapi import FastAPI, Request, Response, HTTPException
import httpx
from pydantic import BaseModel
from .xml_parsing import get_employees_orders, Menu, EmployeeOrder
from .http_reqres import get_menu, post_orders

from .utils import verify_third_party_response

app = FastAPI()



@app.post("/xml")
async def post_read_root(request: Request):
    if request.headers['content-type'] != 'application/xml':
        raise HTTPException(status_code=400, detail="this endpoint accept only format request application/xml")
    
    #Decode body and retrieve EmployeeOrder objects
    body = b'' #xml file
    async for chunk in request.stream():
        body += chunk
    xml_str = body.decode('utf-8')
    employee_orders_list = get_employees_orders(xml_str) #parse xml
    
    #Retrieving menu-json
    menu = None #fetch menu.json
    try:
        menu_response = await get_menu()
        verify_third_party_response(menu_response.status_code)
        menu = Menu(menu_response.json())
    except httpx.TimeoutException:
        ERROR_MESSAGE = "Timeout error calling get menu endpoint"
        print(ERROR_MESSAGE)
        raise HTTPException(status_code=500, detail=ERROR_MESSAGE)
    except TypeError:
        raise HTTPException(status_code=500, detail="Error during parse json response from delivery server")

    try:
        orders_response = await post_orders(employee_orders_list, menu)
        verify_third_party_response(orders_response.status_code)
    except httpx.TimeoutException:
        ERROR_MESSAGE = "Timeout error calling post order endpoint (delivery company)"
        print(ERROR_MESSAGE)
        raise HTTPException(status_code=500, detail=ERROR_MESSAGE)
    
    return {'msg': 'order sent to the delivery company successfully'}
    
    # menu = None #fetch menu.json
    # try:
    #     menu_file = json.loads(read_file('resources/menu.json'))
    #     menu = Menu(menu_file)
    # except ValueError:
    #     print("Can't parsing menu.json")
    #     raise HTTPException(status_code=500, detail="problem while retrieving order.json file")
    


    # orders_json = []
    # for el in employee_orders_list:
    #     if el.is_attending:
    #         orders_json.append(el.get_order(menu))
    # write_json('resources/orders2.json', {'orders': orders_json})    
    


@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}