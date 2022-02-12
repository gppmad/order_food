from typing import Dict, List, Type
import xml.etree.ElementTree as ET
import xmlschema

class Menu():

    def __init__(self, menu: Dict):
        self.menu_json = menu
        
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
            order = {'id': '', 'amount': ''}
            n = el[0]
            text_order = el[3::].strip()
            order['id'] = menu.find_dish_id(text_order)
            order['amount'] = int(n)
            dishes.append(order)
        return dishes

    def get_order(self, menu: Type[Menu]) -> Dict:
        employee_dishes = self.__get_dishes(menu)
        customer = {'name': self.name, 'address': self.address}
        employee_json = {'customer': customer, 'items': employee_dishes}
        return employee_json

def get_employees_orders(xml_file: str) -> List[EmployeeOrder]:
    schema = xmlschema.XMLSchema('resources/xml_validator.xsd')
    result = schema.is_valid(xml_file)

    if result is False:
        raise Exception('XML file not valid')


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
                is_attending = True if employee.text == 'true' else False
            elif employee.tag == 'Order':
                order = employee.text
        # Create object and add it to the list
        order_list.append(EmployeeOrder(name, address, is_attending, order))

    return order_list
