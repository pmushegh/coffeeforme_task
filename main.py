from utils import db_utils

import logging

logging_config = {'filename': 'log/all.log',
                  'filemode': 'a',
                  'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                  'level': 10}

logging.basicConfig(**logging_config)


def main():
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
