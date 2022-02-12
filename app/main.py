import json
from typing import Optional
from fastapi import FastAPI, Request, Response, HTTPException
from pydantic import BaseModel
from .xml_parsing import get_employees_orders, Menu, EmployeeOrder
from .utils import read_file, write_json

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
    
    menu = None #fetch menu.json
    try:
        menu_file = json.loads(read_file('resources/menu.json'))
        menu = Menu(menu_file)
    except ValueError:
        print("Can't parsing menu.json")
        raise HTTPException(status_code=500, detail="problem while retrieving order.json file")
    
    

    orders_json = []
    for el in employee_orders_list:
        if el.is_attending:
            orders_json.append(el.get_order(menu))
    write_json('resources/orders2.json', {'orders': orders_json})    
    
    return {'msg': 'order sent to the delivery company'}


@app.get("/")
def read_root():
    return {"Hello": "World"}
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}