from typing import Optional
from fastapi import FastAPI, Request, HTTPException
from .xml_parsing import get_employees_orders, Menu
from .http_reqres import get_menu, post_orders

app = FastAPI()

@app.post("/send_xml")
async def post_read_root(request: Request):
    if request.headers['content-type'] != 'application/xml':
        raise HTTPException(status_code=400, detail="this endpoint accept only format request application/xml")
    
    #Decode body and retrieve EmployeeOrder objects
    body = b'' #xml file
    async for chunk in request.stream():
        body += chunk
    xml_str = body.decode('utf-8')
    
    try:
        employee_orders_list = get_employees_orders(xml_str) #parse xml
    except Exception:
        raise HTTPException(status_code=400, detail="XML is not valid")

    #Retrieving menu-json
    menu = None #fetch menu.json
    menu_response = await get_menu()
    if menu_response != None:
        menu = Menu(menu_response.json())
    else:
        raise HTTPException(status_code=500, detail="Problem calling get menu endpoint")

    #Sending order
    orders_response = await post_orders(employee_orders_list, menu)
    if orders_response == None:
        raise HTTPException(status_code=500, detail="Timeout error calling post order endpoint (delivery company)")
    
    return {'msg': 'order sent to the delivery company successfully'}

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}