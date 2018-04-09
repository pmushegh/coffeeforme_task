from utils import db_utils

import logging
import os
import json


def seller_interactions():
    print('You are in seller mode.')
    return


def manager_interactions():
    print('You are in manager mode.')
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
            seller_interactions()
            break
        elif role == 'manager':
            logging.info('User in manager mode.')
            manager_interactions()
            break
        else:
            logging.error('User has unexpected role: ' + role)
            print('Role is wrong!')
            break

    db_connection.close_db_connection()
    return


if __name__ == '__main__':
    main()
