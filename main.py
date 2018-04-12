from utils import db_utils
from classes import manager
from classes import seller

import logging
import os
import json
import argparse
import traceback

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
    return


def commandline_working_mode(args, db_connection):
    logger.info('Application entered commandline working mode.')
    if args.role == 'seller':
        logger.info('User is in seller mode.')
        user_seller = seller.Seller(args.name)
        user_seller.interactions_silent(db_connection, args)
    elif args.role == 'manager':
        logger.info('User in manager mode.')
        user_manager = manager.Manager(args.name)
        user_manager.interactions_silent(db_connection)
    else:
        logger.error('User has unexpected role: ' + args.role)
        print('Role is wrong!')
    logger.info('Application exited commandline working mode.')
    return


def interactive_working_mode(db_connection):
    logger.info('Application entered interactive mode.')
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
    logger.info('Application exited interactive mode.')
    return


def main(args):
    # Setup DB connection.
    db_connection = db_utils.DBUtils()
    logger.info('Preparing DB staff.')
    if not db_connection.prepare_db_connection():
        print('Problems with DB, please check log.'
              '\nApplication will exit now.')
        logger.error('Exiting application because of DB problems.')
        return

    if args.name is None:
        interactive_working_mode(db_connection)
    else:
        commandline_working_mode(args, db_connection)

    db_connection.close_db_connection()
    return


if __name__ == '__main__':
    init_log()
    parser = argparse.ArgumentParser(description='CoffeeForMe application.')
    parser.add_argument('-name', metavar='Name', type=str, help='User name')
    parser.add_argument('-role', metavar='Role', type=str, help='User role')
    parser.add_argument('-coffee_type', metavar='Coffee', type=str, help='Coffee type')
    parser.add_argument('-coffee_add_ons', metavar='Coffee add-ons', type=str, help='Coffee add-ons type')
    parser.add_argument('-action', metavar='Action', type=str, help='Seller action[price/save/end]')
    try:
        args_temp = parser.parse_args()
    except SystemExit:
        logger.error('Unable to parse command line arguments: ' + traceback.format_exc())
        print('Problems with commandline arguments parsing, see log for details.')
        exit(1)
    main(args_temp)
