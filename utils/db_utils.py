import mysql.connector
import logging
import json

from mysql.connector import errorcode


def read_db_connection_configuration():
    return json.load(open('configurations/db.json'))


def open_db_connection():
    configuration = read_db_connection_configuration()
    try:
        connection = mysql.connector.connect(**configuration)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            logging.error('Something went wrong during connection to DB.')
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            logging.error('DB doesn\'t exist.')
        else:
            logging.error('Some unexpected error: ' + err.msg)
        connection_info = 'Connection data was: '
        for k, v in configuration.items():
            connection_info += '\n' + ('\t' * 11) + k + ': ' + v
        logging.info(connection_info)
        return None

    logging.info('Connection to DB established.')
    return connection


def close_db_connection(connection):
    connection.close()
    logging.info('DB connection closed.')

