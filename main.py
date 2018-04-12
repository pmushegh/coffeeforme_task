from utils import db_utils
from classes import manager
from classes import seller

import logging
import os
import json

logger = logging.getLogger(__name__)


def input_s(message=''):
    temp = input(message)
    if temp == 'exit':
        print('Application will exit now.')
        logger.info('Exiting application after "exit" command.')
        exit()
    return temp


def init_log():
    # Create directory for log file if it is not exists
    directory = os.path.dirname(os.path.realpath(__file__)) + '/log'
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Setup logging parameters.
    logging_config = json.load(open('configurations/log.json'))
    logging.basicConfig(**logging_config)


def main():
    init_log()

    # Setup DB connection.
    db_connection = db_utils.DBUtils()
    logger.info('Preparing DB staff.')
    if not db_connection.prepare_db_connection():
        print('Problems with DB, please check log.'
              '\nApplication will exit now.')
        logger.error('Exiting application because of DB problems.')
        return

    print('Welcome to CoffeeForMe seller/manager system!\n'
          'To exit any time type "exit".')
    while True:
        user_name = input_s('Input your user name: ')
        logger.info('User name is: ' + user_name)
        if len(user_name) > 40:
            logger.warning('Long user name: ' + user_name)
            print('Please input user name one more time, too long one.')
            continue
        role = input_s('Input your role(seller/manager): ')
        logger.info('Role is: ' + role)
        if role == 'seller':
            logger.info('User is in seller mode.')
            user_seller = seller.Seller(user_name)
            user_seller.interactions(db_connection)
            break
        elif role == 'manager':
            logger.info('User in manager mode.')
            user_manager = manager.Manager(user_name)
            user_manager.interactions(db_connection)
            break
        else:
            logger.error('User has unexpected role: ' + role)
            print('Role is wrong!')
            break

    db_connection.close_db_connection()
    return


if __name__ == '__main__':
    main()
