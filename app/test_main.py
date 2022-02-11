from fastapi.testclient import TestClient
from .main import app
from .xml_parsing import Menu
import utils

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

class TestMenu:

    def test_find_dish_id(self):
        # json_menu = utils.read_file ('../resources/menu.json') 
        # menu = Menu()
        print(utils.__name__) 