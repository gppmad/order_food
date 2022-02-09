import xml.etree.ElementTree as ET
from xmlrpc.client import Boolean

# This class will be moved in another file


class EmployeeOrder():

    def __init__(self, name: str, address: dict, is_attending: Boolean, order: str) -> None:
        self.name = name
        self.address = address
        self.is_attending = is_attending
        self.order = order

    def __str__(self) -> str:
        return f'{self.name} - {self.address} - {self.is_attending} - {self.order}'


def read_file(file: str = 'examples/employee_orders.xml') -> str:
    with open(file, 'r') as file:
        data = file.read().replace('\n', '')
    return data


def employees_orders(xml_file: str) -> list:
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
    l = employees_orders(xml_orders)
    for el in l:
        print(el)
