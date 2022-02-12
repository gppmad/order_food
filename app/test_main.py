from fastapi.testclient import TestClient
import json
import pytest
from .main import app
from .xml_parsing import Menu
from .utils import read_file, write_json
from .http_reqres import get_menu

client = TestClient(app)


class TestApp:

    def test_read_main(self):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"Hello": "World"}

class TestMenu:

    def test_find_dish_id(self):
        menu = None
        try:
            menu_file = json.loads(read_file('resources/bad_menu.json'))
            menu = Menu(menu_file)
            assert menu.find_dish_id('Pizza Quattro Formaggi') == 3
        except ValueError:
            assert False, 'cannot parse input json file'
       
class TestHttpReqRes:

    def t1(self):
        pass