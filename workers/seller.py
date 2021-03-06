"""Seller class inherited form Employee"""
import json
import logging

from workers.employee import Employee
from utils.input_s import input_s


LOGGER = logging.getLogger(__name__)


class Seller(Employee):
    """
    Seller class extends Employee.
    """
    def __init__(self, name):
        Employee.__init__(self, name, 'seller')
        self.coffee_types = dict()
        self.coffee_add_on_types = dict()

    def read_configs(self):
        """
        Initializes coffee_types and coffee_add_on_types based on json configs.
        :return:
        """
        LOGGER.info('Reading coffee and add-on types configuration.')
        self.coffee_types = json.load(open("configurations/coffee_types.json"))
        self.coffee_add_on_types = json.load(open("configurations/coffee_add_on_types.json"))
        return

    def get_add_ons_price(self, coffee_add_ons):
        """
        Gets coffee add-ons total price, calls get_add_ons_total_price().
        :param coffee_add_ons: coffee_add_ons string
        :return: Coffee add-ons total price, in case of problem None.
        """
        total_price = 0
        if coffee_add_ons != '':
            coffee_add_ons = coffee_add_ons.split(',')
            add_ons_price = self.get_add_ons_total_price(coffee_add_ons)
            if add_ons_price is None:
                LOGGER.error('Problems with add-ons.')
                return None
            else:
                total_price += add_ons_price
            return total_price
        else:
            return 0.0

    def perform_action(self, action, db_connection, total_price):
        """
        Perform provide action(show sale price, save sale, exit).
        :param action: action name(price, save, end)
        :param db_connection: DBUtils type object
        :param total_price: sale total price
        :return: In case of success returns True, in case of any problem False.
        """
        if action == 'price':
            LOGGER.info('Showing price.')
            print('Price is ' + str(total_price))
        elif action == 'save':
            LOGGER.info('Saving sale to DB.')
            if not db_connection.update_seller_sale_statistics(self.name, total_price):
                return False
            print('Sale saved to DB.')
            return False
        elif action == 'end':
            LOGGER.info('Exiting seller interactions.')
            print('Exiting seller interactions.')
            return False
        else:
            LOGGER.info('Unknown action is provided: %s', action)
            print('Wrong action!')
        return True

    def interactions_silent(self, db_connection, args):
        """
        Seller interaction base on commandline arguments.
        :param db_connection: DBUtils type object
        :param args: commandline arguments
        :return:
        """
        self.read_configs()
        total_price = 0.0

        if not db_connection.check_seller_existence(self.name):
            print('Problems with user check, see log for more details.')
            return

        # Coffee selection
        coffee_type_price = self.coffee_types.get(args.coffee_type)
        if coffee_type_price is None:
            print('Wrong coffee type is selected.')
            LOGGER.error('Unknown coffee type was selected.')
            return
        else:
            total_price += self.coffee_types.get(args.coffee_type)

        # Coffee add-on selection
        LOGGER.info('Getting add-ons price')
        add_ons_price = self.get_add_ons_price(args.coffee_add_ons)
        if add_ons_price is None:
            print('Problem with add-ons.')
            return
        else:
            total_price += add_ons_price

        self.perform_action(args.action, db_connection, total_price)

        return

    def interactions(self, db_connection):
        """
        Seller interaction base on commandline user interactions.
        :param db_connection: DBUtils type object
        :return:
        """
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
            LOGGER.error('Unknown coffee type was selected.')
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
        LOGGER.info('Getting add-ons price')
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

    def get_add_ons_total_price(self, add_ons):
        """
        Calculated add-ons total price.
        :param add_ons: add-ons list
        :return: add-ons total price, in case of problem None.
        """
        total_price = 0.0
        for add_on_item in add_ons:
            price = self.coffee_add_on_types.get(add_on_item)
            if price is None:
                LOGGER.error('Unknown add-on: %s', add_on_item)
                return None
            else:
                total_price += price
        return price
