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
            sql = 'CREATE TABLE `' + self.db_configuration['database'] + '`.`sales` ' \
                  '(`seller_name` VARCHAR(40) NOT NULL,`number_of_sales` INT NOT NULL,' \
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
        try:
            db_cursor = self.db_connection.cursor()
            db_cursor.execute('CREATE SCHEMA ' + db_name)
            db_cursor.close()
            return True
        except mysql.connector.Error as err:
            logging.error('Error during DB schema creation: ' + err.msg)
            db_cursor.close()
            return False

    def get_data_from_sales_table(self):
        try:
            db_cursor = self.db_connection.cursor()
            db_cursor.execute('SELECT * FROM sales')
            result = db_cursor.fetchall()
            db_cursor.close()
            return result
        except mysql.connector.Error as err:
            logging.error('Problems during getting Sales table data: ' + err.msg)
            return None

    def add_empty_seller_to_db(self, seller_name):
        try:
            sql = 'INSERT INTO `' + self.db_configuration['database'] + '`.`sales` (`seller_name`,' \
                  ' `number_of_sales`, `total_value`) VALUES (\'' + seller_name + '\', \'0\', \'0\')'
            db_cursor = self.db_connection.cursor()
            db_cursor.execute(sql)
            db_cursor.close()
            self.db_connection.commit()
            logging.info('Seller ' + seller_name + ' empty data added to DB.')
            return True
        except mysql.connector.Error as err:
            logging.error('Error during empty seller adding to DB: ' + err.msg)
            return False

    def check_seller_existence(self, seller_name):
        try:
            sql = 'SELECT COUNT(*) FROM sales WHERE seller_name="' + seller_name + '"'
            db_cursor = self.db_connection.cursor()
            db_cursor.execute(sql)
            record_number = db_cursor.fetchone()[0]
            db_cursor.close()
            if record_number == 1:
                logging.info('User with name - ' + seller_name + ' exists, no need in new record creation.')
            else:
                logging.info('Adding user - ' + seller_name + ' to DB.')
                if not self.add_empty_seller_to_db(seller_name):
                    return False
            return True
        except mysql.connector.Error as err:
            logging.error('Some problems during user existence check: ' + err.msg)
            db_cursor.close()
            return False
