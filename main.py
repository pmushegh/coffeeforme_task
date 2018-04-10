from utils import db_utils

import logging
import os
import json


def seller_interactions(db_connection, seller_name):
    print('You are in seller mode.')
    if not db_connection.check_seller_existence(seller_name):
        return
    if not db_connection.update_seller_sale_statistics(seller_name, 20.3, 10):
        return
    return


def manager_interactions(db_connection):
    print('You are in manager mode.')
    all_sale_data = db_connection.get_data_from_sales_table()
    if all_sale_data is None:
        print('Problems with getting sales data.'
              '\nApplication will exit now.')
    else:
        total_sales_value = 0.0
        print('|' + '-' * 82 + '|')
        print('|Sales data:' + ' ' * 71 + '|')
        print('|' + '-' * 82 + '|')
        print('|{0:40}|{1:20}|{2:20}|'.format('Seller name', 'Number of sales', 'Total Value ($)'))
        print('|' + '-' * 82 + '|')
        for seller, sales_num, total_value in all_sale_data:
            total_sales_value += total_value
            print('|{0:40}|{1:20d}|{2:20}|'.format(seller, sales_num, total_value))
            print('|' + '-' * 82 + '|')
        print('|'+' ' * 40 + '|' + ' ' * 20 + '|{0:20}|'.format('Total:' + str(total_sales_value)))
        print('|' + '-' * 82 + '|')
    return


def main():
    # Create directory for log file if it is not exists
    directory = os.path.dirname(os.path.realpath(__file__)) + '/log'
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Setup logging parameters.
    logging_config = json.load(open('configurations/log.json'))
    logging.basicConfig(**logging_config)

    # Setup DB connection.
    db_connection = db_utils.DBUtils()
    if not db_connection.open_db_connection():
        logging.error('No DB connection is established.')
        print('Problems with DB, please check log.'
              '\nApplication will exit now.')
        return
    if not db_connection.check_db():
        logging.error('Problems during DB check, please check log.')
        print('Problems during DB check, please check log.'
              '\nApplication will exit now.')
        return
    if not db_connection.check_sales_table():
        logging.error('Problems with Sales table, please check log.')

    while True:
        user_name = input('Welcome to CoffeeForMe seller/manager system!'
                          '\nInput your user name: ')
        logging.info('User name is: ' + user_name)
        role = input('Input your role(seller/manager): ')
        logging.info('Role is: ' + role)
        if role == 'seller':
            logging.info('User is in seller mode.')
            seller_interactions(db_connection, user_name)
            break
        elif role == 'manager':
            logging.info('User in manager mode.')
            manager_interactions(db_connection)
            break
        else:
            logging.error('User has unexpected role: ' + role)
            print('Role is wrong!')
            break

    db_connection.close_db_connection()
    return


if __name__ == '__main__':
    main()
