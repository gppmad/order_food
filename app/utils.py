import json
from typing import Dict
from fastapi import HTTPException

def read_file(file: str) -> str:
    with open(file, 'r') as file:
        data = file.read().replace('\n', '')
    return data


def write_json(file: str, data=Dict):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)


def verify_third_party_response(status_code):
    if status_code >= 500:
        raise HTTPException(
            status_code=503, detail="Delivery company service unavailable")
    if status_code != 200:
        raise HTTPException(
            status_code=500, detail="Error during the connection with the delivery company")
