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