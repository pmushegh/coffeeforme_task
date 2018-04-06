import mysql.connector

from mysql.connector import errorcode

configuration = {'user': 'reader',
                 'password': '123456789',
                 'host': '127.0.0.1',
                 'database': 'coffeeformedb'}


def open_db_connection():
    try:
        connection = mysql.connector.connect(**configuration)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Something went wrong during connection to DB.')
        elif err.errno == errorcode.EN_BAD_DB_ERROR:
            print('DB doesn\'t exist.')
        else:
            print('Some unexpected error: ' + err)
        return ''

    return connection


def close_db_connection(connection):
    connection.close()

