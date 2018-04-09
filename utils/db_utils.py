import mysql.connector
import logging
import json

from mysql.connector import errorcode


class DBUtils:
    def __init__(self):
        self.db_configuration = json.load(open('configurations/db.json'))
        logging.info('DB connection configuration is: ')
        logging.info(self.db_configuration)
        self.db_connection = mysql.connector.MySQLConnection()

    def open_db_connection(self):
        try:
            self.db_connection = mysql.connector.connect(user=self.db_configuration['user'],
                                                         password=self.db_configuration['password'],
                                                         host=self.db_configuration['host'])
            logging.info('Connection to DB established.')
            return True
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                logging.error('DB access error. Message: ' + err.msg)
            else:
                logging.error('Some unexpected error during connection to MySQL: ' + err.msg)
            return False

    def check_db(self):
        try:
            self.db_connection.database = self.db_configuration['database']
            return True
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                logging.warning('DB' + self.db_configuration['database'] + ' doesn\'t exist.')
                self.db_connection = mysql.connector.connect(**self.db_configuration)
                logging.info('Creating DB ' + self.db_configuration['database'])
                if self.create_db_schema(self.db_configuration['database']):
                    return True
                else:
                    return False
            else:
                logging.error('Some unexpected error during DB creation: ' + err.msg)
                return False

    def check_sales_table(self):
        try:
            sql = 'SELECT COUNT(*) FROM information_schema.tables WHERE table_name="sales"'
            db_cursor = self.db_connection.cursor()
            db_cursor.execute(sql)
            if db_cursor.fetchone()[0] == 1:
                db_cursor.close()
                return True
            else:
                if self.create_sales_table():
                    db_cursor.close()
                    return True
                else:
                    return False
        except mysql.connector.Error as err:
            logging.error('Some unexpected error during Sales table check: ' + err.msg)
            return False

    def create_sales_table(self):
        try:
            sql = 'CREATE TABLE `coffeeformedb`.`sales` (`seller_name` VARCHAR(100) NOT NULL,' \
                  '`number_of_sales` INT NOT NULL,' \
                  '`total_value` DOUBLE NOT NULL,PRIMARY KEY (`seller_name`));'
            db_cursor = self.db_connection.cursor()
            db_cursor.execute(sql)
            db_cursor.close()
            logging.info('Salas table created.')
            return True
        except mysql.connector.Error as err:
            logging.error('Some unexpected error during Sales table creation: ' + err.msg)
            return False

    def close_db_connection(self):
        self.db_connection.close()
        logging.info('DB connection closed.')

    def create_db_schema(self, db_name):
        db_cursor = self.db_connection.cursor()
        try:
            db_cursor.execute('CREATE SCHEMA ' + db_name)
            db_cursor.close()
            return True
        except mysql.connector.Error as err:
            logging.error('Error during DB schema creation: ' + err.msg)
            db_cursor.close()
            return False

    def get_data_from_sales_table(self):
        db_cursor = self.db_connection.cursor()
        db_cursor.execute('SELECT * FROM sales')
        result = db_cursor.fetchone()
        return
