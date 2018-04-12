from classes import employee
from main import input_s

import json
import logging

logger = logging.getLogger(__name__)


class Seller(employee.Employee):
    def __init__(self, name):
        super().__init__(name, 'seller')
        self.coffee_types = dict()
        self.coffee_add_on_types = dict()

    def read_configs(self):
        logger.info('Reading coffee and add-on types configuration.')
        self.coffee_types = json.load(open("configurations/coffee_types.json"))
        self.coffee_add_on_types = json.load(open("configurations/coffee_add_on_types.json"))
        return

    def get_add_ons_price(self, coffee_add_ons) -> float:
        total_price = 0
        if coffee_add_ons != '':
            coffee_add_ons = coffee_add_ons.split(',')
            add_ons_price = self.check_inputted_add_ons_and_get_total_price(coffee_add_ons)
            if add_ons_price is None:
                logger.error('Problems with add-ons.')
                return None
            else:
                total_price += add_ons_price
            return total_price
        else:
            return 0.0

    def perform_action(self, action, db_connection, total_price) -> bool:
        if action == 'price':
            logger.info('Showing price.')
            print('Price is ' + str(total_price))
        elif action == 'save':
            logger.info('Saving sale to DB.')
            if not db_connection.update_seller_sale_statistics(self.name, total_price):
                return False
            print('Sale saved to DB.')
            return False
        elif action == 'end':
            logger.info('Exiting seller interactions.')
            print('Exiting seller interactions.')
            return False
        else:
            logger.info('Unknown action is provided: ' + action)
            print('Wrong action!')
        return True

    def interactions_silent(self, db_connection, args):
        self.read_configs()
        total_price = 0.0

        if not db_connection.check_seller_existence(self.name):
            print('Problems with user check, see log for more details.')
            return

        # Coffee selection
        coffee_type_price = self.coffee_types.get(args.coffee_type)
        if coffee_type_price is None:
            print('Wrong coffee type is selected.')
            logger.error('Unknown coffee type was selected.')
            return
        else:
            total_price += self.coffee_types.get(args.coffee_type)

        # Coffee add-on selection
        logger.info('Getting add-ons price')
        add_ons_price = self.get_add_ons_price(args.coffee_add_ons)
        if add_ons_price is None:
            print('Problem with add-ons.')
            return
        else:
            total_price += add_ons_price

        self.perform_action(args.action, db_connection, total_price)

        return

    def interactions(self, db_connection):
        self.read_configs()
        total_price = 0.0

        print('You are in seller mode.')
        if not db_connection.check_seller_existence(self.name):
            print('Problems with user check, see log for more details.')
            return

        # Coffee selection
        coffee_types_message = 'Please select coffee('
        for item in self.coffee_types:
            coffee_types_message += (item + ', ')
        coffee_types_message = coffee_types_message[:-2] + '):'
        coffee_type = input_s(coffee_types_message)
        coffee_type_price = self.coffee_types.get(coffee_type)
        if coffee_type_price is None:
            print('Wrong coffee type is selected.')
            logger.error('Unknown coffee type was selected.')
            return
        else:
            total_price += self.coffee_types.get(coffee_type)

        # Coffee add-on selection
        coffee_add_on_types_message = 'Please select coffee add-ons('
        for item in self.coffee_add_on_types:
            coffee_add_on_types_message += (item + ', ')
        coffee_add_on_types_message = coffee_add_on_types_message[:-2] + ').\n'
        coffee_add_on_types_message += 'Add-ons should be separated by ","(exp. "sugar,milk"):'
        coffee_add_ons = input_s(coffee_add_on_types_message)
        logger.info('Getting add-ons price')
        add_ons_price = self.get_add_ons_price(coffee_add_ons)
        if add_ons_price is None:
            print('Problem with add-ons.')
            return
        else:
            total_price += add_ons_price

        print('For showing sale total price type "price",\n'
              'to save sale - "save", to finish interactions "end"')
        while True:
            action = input_s()
            if not self.perform_action(action, db_connection, total_price):
                return
        return

    def check_inputted_add_ons_and_get_total_price(self, add_ons) -> float:
        total_price = 0.0
        for add_on_item in add_ons:
            price = self.coffee_add_on_types.get(add_on_item)
            # with self.coffee_add_on_types.get(add_on_item) as price:
            if price is None:
                logger.error('Unknown add-on: ' + add_on_item)
                return None
            else:
                total_price += price
        return price
