from utils import db_utils

import logging
import os
import json


def main():
    # Create directory for log file if it is not exists
    directory = os.path.dirname(os.path.realpath(__file__)) + '/log'
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Setup logging parameters.
    logging_config = json.load(open('configurations/log.json'))
    logging.basicConfig(**logging_config)

    # Setup DB connection.
    connection = db_utils.open_db_connection()
    if connection is None:
        logging.error('No DB connection is established.')
        print('Something went wrong during DB connection, please check log.'
              '\nApplication will exit now.')
        return

    while True:
        user_name = input('Welcome to CoffeeForMe seller/manager system!'
                          '\nInput your user name: ')
        logging.info('User name is: ' + user_name)
        role = input('Input your role(seller/manager): ')
        logging.info('Role is: ' + role)
        if role == 'seller':
            logging.info('User is in seller mode.')
            print('You are in seller mode.')
            break
        elif role == 'manager':
            logging.info('User in manager mode.')
            print('You are in manager mode.')
            break
        else:
            logging.error('User has unexpected role: ' + role)
            print('Role is wrong!')
            break

    db_utils.close_db_connection(connection)


if __name__ == '__main__':
    main()
