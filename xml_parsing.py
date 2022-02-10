from asyncore import read
from typing import Dict, List, Type
import xml.etree.ElementTree as ET
import json
from xmlrpc.client import Boolean

# This class will be moved in another file

class Menu():

    def __init__(self, menu: Dict):
        self.menu = json.loads(menu)

    def find_dish_id(self, name: str):
        dishes_list = self.menu['dishes']
        for el in dishes_list:
            if el['name'].strip() == name.strip():
                return el['id']
        return None
class EmployeeOrder():

    def __init__(self, name: str, address: Dict, is_attending: bool, order: str) -> None:
        self.name = name
        self.address = address
        self.is_attending = is_attending
        self.order = order

    def __str__(self) -> str:
        return f'{self.name} - {self.address} - {self.is_attending} - {self.order}'

    def __get_dishes(self, menu: Type[Menu]) -> Dict:
        str_ordered = self.order
        list_orders = [el.strip() for el in str_ordered.split(',')]
        orders_dict = {}
        for el in list_orders:
            n = el[0]
            text_order = el[3::].strip()
            orders_dict[text_order] = n
        return orders_dict

    def get_json_order(self) -> Dict:
        customer = {'full_name': self.name, 'address': self.address}
        employee_json = {'customer': customer, 'dishes': ''}
        employee_dishes = self.__get_dishes()
        return employee_dishes





def read_file(file: str = 'examples/employee_orders.xml') -> str:
    with open(file, 'r') as file:
        data = file.read().replace('\n', '')
    return data


def get_employees_orders(xml_file: str) -> List[EmployeeOrder]:
    root = ET.fromstring(xml_file)
    order_list = []

    for employees in root:
        name = ''
        address = {'street': '', 'city': '', 'postal_code': ''}
        is_attending = False
        order = ''
        for employee in employees:
            if employee.tag == 'Name':
                name = employee.text
            elif employee.tag == 'Address':
                for address_fields in employee:  # Drill down on Address
                    if address_fields.tag == 'Street':
                        address['street'] = address_fields.text
                    elif address_fields.tag == 'City':
                        address['city'] = address_fields.text
                    elif address_fields.tag == 'PostalCode':
                        address['postal_code'] = address_fields.text
            elif employee.tag == 'IsAttending':
                is_attending = employee.text
            elif employee.tag == 'Order':
                order = employee.text
        # Create object and add it to the list
        order_list.append(EmployeeOrder(name, address, is_attending, order))

    return order_list


if __name__ == "__main__":
    xml_orders = read_file()
    menu_json = read_file('examples/menu.json')
    menu = Menu(menu_json)
    l = get_employees_orders(xml_orders)
    for el in l:
        print(el.get_json_order())
