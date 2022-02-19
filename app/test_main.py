from pytest import raises
import respx
import json

from .main import app
from .xml_parsing import Menu
from .utils import read_file
from .http_reqres import BASE_URL, get_menu
from httpx import Response

class TestApp:

    @respx.mock
    def test_get_menu(self):
            my_route = respx.get("http://localhost:3000").mock(return_value=Response(200))
            response = get_menu()
            assert my_route.called
            assert response.status_code  == 200 

    @respx.mock
    def test_get_menu_none(self):
            my_route = respx.get("http://localhost:3000").mock(return_value=Response(400))
            response = get_menu()
            assert my_route.called
            assert response == None 
class TestMenu:

    def test_find_dish_id(self):
        menu = None
        menu_file = json.loads(read_file('resources/menu.json'))
        menu = Menu(menu_file)
        assert menu.find_dish_id('Pizza Quattro Formaggi') == 3

    def test_bad_way_find_dish_id(self):
        with raises (json.JSONDecodeError):
            menu_file = json.loads(read_file('resources/bad_menu.json'))
        