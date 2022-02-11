import json
from typing import Dict

def read_file(file: str) -> str:
    with open(file, 'r') as file:
        data = file.read().replace('\n', '')
    return data


def write_json(file: str, data=Dict):

    with open(file, 'w') as f:
        json.dump(data, f, indent=4)
