# Description
Simple app that receives an XML file as request and makes a food order through a HTTP JSON Request to a third part delivery company.

This project is built with FAST API.
- - - 
## Requirements
In this project I used Python 3.8 with the latest version of [fastAPI](https://fastapi.tiangolo.com/), [pytest](https://docs.pytest.org/en/7.0.x/),  [httpx](https://www.python-httpx.org/) and [uvicorn](https://www.uvicorn.org/) as ASGI implementation server.

You can find further details inside requirements.txt.

If you want to run without Docker please take a look at the section "Run with Uvicorn".

How to use it? Send the employee_orders XML file to {base_url}/send_xml.\
Here's an example:

```
curl -X 'POST' \
  'http://{base_url}/send_xml' \
  -H 'accept: application/xml' \
  -H 'Content-Type: application/xml' \
  -d @employee_orders.xml
```

## Run with docker 

```
docker build -t order_food . 
docker run --name order_food_container -p 80:80 -e BASE_URL="http://{ENDPOINT_MOCK_SERVER}:{PORT_MOCK_SERVER}" order_food

```

## Run with Uvicorn 
Clone this project and move inside the folder with a local python 3.8 virtual environment:

```
cd order_food
python3 -m venv venv
source venv/bin/activate
pip install --no-cache-dir --upgrade -r requirements.txt
```
Export the third part delivery company's endpoint running the following command. 

```
export BASE_URL="http://{ENDPOINT_MOCK_SERVER}:{PORT_MOCK_SERVER}"
```
Then, run:

```
uvicorn app.main:app --reload
```

- - - 
## Problems encountered

There are few differences between the order.json written in your pdf and the other order.json that you provide me as file.

Differences:
- orders.customer.name (orders.customer.full_name in PDF)
- orders.items (orders.dished in PDF)
- orders.dishes.id (orders.dishes.dish_id)

I followed the structure in the order.json that you provided.

## Test
Run app test with:

```
pytest -s app/test_main.py --asyncio-mode=strict
```

----
## Tasks TODO:

- Using Logger (I had few problems to use it inside FastAPI I need more time to check it)\
- Improve testing with pytest
- Improve code quality with [Python type hints](https://docs.python.org/3/library/typing.html)