"""Application main module"""
import logging
import os
import json
import argparse
import traceback

from utils.db_utils import DBUtils
from utils.input_s import input_s
from workers.manager import Manager
from workers.seller import Seller

LOGGER = logging.getLogger(__name__)


def init_argument_parser():
    """
    Initializing argument parser for command line.
    :return:
    """
    parser = argparse.ArgumentParser(description='CoffeeForMe application.')
    parser.add_argument('-n', '--name',
                        dest='name',
                        type=str,
                        help='User name')
    parser.add_argument('-r', '--role',
                        dest='role',
                        type=str,
                        help='User role')
    parser.add_argument('-c_t', '--coffee_type',
                        dest='coffee_type',
                        type=str,
                        help='Coffee type')
    parser.add_argument('-c_as', '--coffee_add_ons',
                        dest='coffee_add_ons',
                        type=str,
                        help='Coffee add-ons type')
    parser.add_argument('-a', '--action',
                        dest='action',
                        type=str,
                        help='Seller action[price/save/end]')
    return parser


def parse_arguments(parser):
    """
    Parse commandline arguments. In case of problem during parsing triggers application exit.
    :param parser: parser object
    :return: parsed commandline arguments
    """
    try:
        args_temp = parser.parse_args()
    except SystemExit:
        LOGGER.error('Unable to parse command line arguments: %s', traceback.format_exc())
        print('Problems with commandline arguments parsing, see log for details.')
        exit(1)
    return args_temp


def init_log():
    """
    Initialized log configuration, and creates "log" folder.
    :return:
    """
    # Create directory for log file if it is not exists
    directory = os.path.dirname(os.path.realpath(__file__)) + '/log'
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Setup logging parameters.
    logging_config = json.load(open('configurations/log.json'))
    logging.basicConfig(**logging_config)
    return


def commandline_working_mode(args, db_connection):
    """
    Provides interactions with system based on commandline arguments.
    :param args: commandline arguments
    :param db_connection: DBUtils type object
    :return:
    """
    LOGGER.info('Application entered commandline working mode.')
    if args.role is None:
        print('--role commandline argument is not provided.')
        LOGGER.error('--role commandline argument is not provided.')
        return
    if args.role == 'seller':
        LOGGER.info('User is in seller mode.')
        user_seller = Seller(args.name)
        user_seller.interactions_silent(db_connection, args)
    elif args.role == 'manager':
        LOGGER.info('User in manager mode.')
        user_manager = Manager(args.name)
        user_manager.interactions_silent(db_connection)
    else:
        LOGGER.error('User has unexpected role: %s', args.role)
        print('Role is wrong!')
    LOGGER.info('Application exited commandline working mode.')
    return


def interactive_working_mode(db_connection):
    """
    Provides interactions with system based on commandline user interaction.
    :param db_connection: DBUtils type object
    :return:
    """
    LOGGER.info('Application entered interactive mode.')
    print('Welcome to CoffeeForMe seller/manager system!\nTo exit any time type "exit".')
    while True:
        user_name = input_s('Input your user name: ')
        LOGGER.info('User name is: %s', user_name)
        if len(user_name) > 40:
            LOGGER.warning('Long user name: %s', user_name)
            print('Please input user name one more time, too long one.')
            continue
        role = input_s('Input your role(seller/manager): ')
        LOGGER.info('Role is: %s', role)
        if role == 'seller':
            LOGGER.info('User is in seller mode.')
            user_seller = Seller(user_name)
            user_seller.interactions(db_connection)
            break
        elif role == 'manager':
            LOGGER.info('User in manager mode.')
            user_manager = Manager(user_name)
            user_manager.interactions(db_connection)
            break
        else:
            LOGGER.error('User has unexpected role: %s', role)
            print('Role is wrong!')
            break
    LOGGER.info('Application exited interactive mode.')
    return


def main():
    """
    Application base function.
    :return:
    """
    init_log()

    args = parse_arguments(init_argument_parser())

    # Setup DB connection.
    db_connection = DBUtils()
    LOGGER.info('Preparing DB staff.')
    if not db_connection.prepare_db_connection():
        print('Problems with DB, please check log.\nApplication will exit now.')
        LOGGER.error('Exiting application because of DB problems.')
        return

    try:
        if args.name is None:
            interactive_working_mode(db_connection)
        else:
            commandline_working_mode(args, db_connection)
        db_connection.close_db_connection()
    except UserWarning as err:
        LOGGER.warning(err)
        db_connection.close_db_connection()

    return


if __name__ == '__main__':
    main()
