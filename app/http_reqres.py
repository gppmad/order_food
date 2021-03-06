import httpx
import os
import logging

logger = logging.getLogger("uvicorn.error")
BASE_URL = os.environ.get('BASE_URL', 'http://localhost:3000')

def get_menu():
    endpoint = f"{BASE_URL}/menu"
    response = None
    try:
        response = httpx.get(endpoint)
        logger.info(f"Menu retrivied from {BASE_URL}")
    except httpx.TimeoutException as exc:
        logger.error(f"Timeout calling {endpoint}")
    except httpx.RequestError as exc:
        logger.error(f"An error occurred while requesting {exc.request.url!r}.")
    except httpx.HTTPStatusError as exc:
        logger.error(f"Error response {exc.response.status_code} while requesting {exc.request.url!r}.")

    if response is None or response.status_code != 200:
        logger.error(f"Problem calling get menu endpoint {endpoint}")
        return None

    return response


def post_orders(employee_orders_list, menu):
    orders_json = []
    for el in employee_orders_list:
        if el.is_attending:
            orders_json.append(el.get_order(menu))
    endpoint = f"{BASE_URL}/bulk/order"
    headers = {'content-type':'application/json','accept':'application/json'}

    try:
        response = httpx.post(endpoint, json={'orders': orders_json}, headers=headers)
    except httpx.TimeoutException as exc:
        logger.error(f"Timeout calling {endpoint}")    
    except httpx.RequestError as exc:
        logger.error(f"An error occurred while requesting {exc.request.url!r}.")
    except httpx.HTTPStatusError as exc:
        logger.error(f"Error response {exc.response.status_code} while requesting {exc.request.url!r}.")

    if response is None or response.status_code != 200:
        logger.error(f"Problem calling send order endpoint {endpoint}")
        return None

    return response