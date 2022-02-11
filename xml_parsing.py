from asyncore import read
from typing import Dict, List, Type
import xml.etree.ElementTree as ET
import json
from xmlrpc.client import Boolean

# This class will be moved in another file


class Menu():

    def __init__(self, menu: str):
        self.menu_json = json.loads(menu)

    def find_dish_id(self, name: str):
        dishes_list = self.menu_json['dishes']
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

    def __get_dishes(self, menu: Type[Menu]) -> List[Dict]:
        str_ordered = self.order
        list_orders = [el.strip() for el in str_ordered.split(',')]
        dishes = []
        for el in list_orders:
            order = {'dish_id': '', 'amount': ''}
            n = el[0]
            text_order = el[3::].strip()
            order['dish_id'] = menu.find_dish_id(text_order)
            order['amount'] = n
            dishes.append(order)
        return dishes

    def get_order(self, menu: Type[Menu]) -> Dict:
        employee_dishes = self.__get_dishes(menu)
        customer = {'full_name': self.name, 'address': self.address}
        employee_json = {'customer': customer, 'dishes': employee_dishes}
        return employee_json



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

def read_file(file: str = 'examples/employee_orders.xml') -> str:
    with open(file, 'r') as file:
        data = file.read().replace('\n', '')
    return data


def write_json(file: str = 'examples/orders.json', data=Dict):
    with open(file, 'w') as f:
        json.dump(data, f,indent=4)


if __name__ == "__main__":
    xml_orders = read_file()
    menu = Menu(read_file('examples/menu.json'))
    l = get_employees_orders(xml_orders)
    # print(l[0].get_json_order(menu))
    orders = []
    for el in l:
        orders.append(el.get_order(menu))

    write_json('examples/orders2.json', {'orders': orders})
