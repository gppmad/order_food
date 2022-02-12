# Description
Simple app that receive an XML file as request and make an order food based with a JSON Request to a third part delivery company.

This project is built with FAST API.
- - - 
## Requirements
In this project I used Python 3.8 with the latest version of fastAPI, pytest, httpx and uvicorn as ASGI implementation server.

You can find further details inside requirements.txt
If you want to run without Docker please take a look at the section Run with Uvicorn.

## Run with docker 

```
docker build -t order_food . 
docker run --name order_food_container -p 80:80 order_food

```

## Run with Uvicorn 
Clone this project and cd inside the folder with a local python 3.8 virtual environment:

```
cd order_food
python3 -m venv venv
pip install --no-cache-dir --upgrade -r requirements.txt
```
Export the third part delivery company endpoint running the following command. 

```
export BASE_URL="nourish.me/api/v1"
```
Then 

```
uvicorn app.main:app --reload
```

- - - 
## Problems encountered

1) There is a difference from the order.json written in your pdf and the other order.json that you provide me as file.
    Fields: 
        orders.customer.name (orders.customer.full_name in PDF)
        orders.items (orders.dished in PDF)
        orders.dishes.id (orders.dishes.dish_id)

----
## Tasks TODO:

- Using Logger (I had few problems to use it inside FastAPI I need more time to check it)\
- Improve testing with pytest
-HTTP Connection problem inside Docker File