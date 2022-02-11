# Description
Simple app that allow me to order food on behalf of my company.\
This project is built with fast api.

## Run with docker 

```
docker build -t order_food . 
docker run --name order_food_container -p 80:80 order_food
```

## Run without Docker 

```
uvicorn app.main:app --reload
```

## Problem

1) There is a difference from the order.json written in your pdf and the other order.json that you provide me as file.
    Fields: 
        orders.customer.name (orders.customer.full_name in PDF)
        orders.items (orders.dished in PDF)
        orders.dishes.id (orders.dishes.dish_id)