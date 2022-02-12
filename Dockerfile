FROM python:3.8

WORKDIR /code

ENV BASE_URL="localhost:3000"

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

COPY ./resources /code/resources

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]