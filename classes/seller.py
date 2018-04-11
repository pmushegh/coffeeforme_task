from classes import employee

from main import input_s
import json
import logging


class Seller(employee.Employee):
    def __init__(self, name):
        super().__init__(name, 'seller')

    def interactions(self, db_connection):
        logging.info('Reading coffee and add-on types configuration.')
        coffee_types = json.load(open("configurations/coffee_types.json"))
        coffee_add_on_types = json.load(open("configurations/coffee_add_on_types.json"))
        total_price = 0.0

        print('You are in seller mode.')
        if not db_connection.check_seller_existence(self.name):
            print('Problems with user check, see log for more details.')
            return

        # Coffee selection
        coffee_types_message = 'Please select coffee('
        for item in coffee_types:
            coffee_types_message += (item + ', ')
        coffee_types_message = coffee_types_message[:-2] + '):'
        coffee_type = input_s(coffee_types_message)
        coffee_type_price = coffee_types.get(coffee_type)
        if coffee_type_price is None:
            print('Wrong coffee type is selected.')
            return
        else:
            total_price += coffee_types.get(coffee_type)

        # Coffee add-on selection
        coffee_add_on_types_message = 'Please select coffee add-ons('
        for item in coffee_add_on_types:
            coffee_add_on_types_message += (item + ', ')
        coffee_add_on_types_message = coffee_add_on_types_message[:-2] + ').\n'
        coffee_add_on_types_message += 'Add-ons should be separated by ","(exp. "sugar,milk"):'
        print(coffee_add_on_types_message)
        coffee_add_ons = input_s()
        coffee_add_ons = coffee_add_ons.split(',')

        if not db_connection.update_seller_sale_statistics(self.name, total_price):
            return
        return
