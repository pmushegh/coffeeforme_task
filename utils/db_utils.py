import mysql.connector
import logging
import json
import traceback

from mysql.connector import errorcode


class DBUtils:
    def __init__(self):
        """
        Reads json configuration for connection to MySQL DB.
        """
        self.logger = logging.getLogger(__name__)
        self.logger.info('Reading DB configuration.')
        self.db_configuration = json.load(open('configurations/db.json'))
        self.logger.info('DB connection configuration is: ')
        self.logger.info(self.db_configuration)
        self.db_connection = mysql.connector.MySQLConnection()

    def open_db_connection(self):
        """
        Setups connection to MySQL DB.
        :return: In case of success returns True, in case of any problem False.
        """
        try:
            self.logger.info('Establishing connection to MySQL.')
            self.db_connection = mysql.connector.connect(user=self.db_configuration['user'],
                                                         password=self.db_configuration['password'],
                                                         host=self.db_configuration['host'])
            self.logger.info('Connection to MySQL established.')
            return True
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                self.logger.error('DB access error. Message:"\n' + traceback.format_exc())
            else:
                self.logger.error('Some unexpected error during connection to MySQL:"\n' + traceback.format_exc())
            return False

    def check_db(self):
        """
        Check connection to DB, in case of if DB not available calls create_db_schema().
        :return: In case of success returns True, in case of any problem False.
        """
        try:
            self.logger.info('Setting DB name for connection.')
            self.db_connection.database = self.db_configuration['database']
            self.logger.info('DB name for connection set.')
            return True
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                self.logger.warning('DB ' + self.db_configuration['database'] + ' doesn\'t exist.')
                self.db_connection = mysql.connector.connect(user=self.db_configuration['user'],
                                                             password=self.db_configuration['password'],
                                                             host=self.db_configuration['host'])
                self.logger.info('Creating DB ' + self.db_configuration['database'])
                if self.create_db_schema(self.db_configuration['database']):
                    self.logger.info('DB created.')
                    self.logger.info('Setting DB name for connection.')
                    self.db_connection.database = self.db_configuration['database']
                    self.logger.info('DB name for connection set.')
                    return True
                else:
                    self.logger.error('DB not created.')
                    self.db_connection.close()
                    return False
            else:
                self.logger.error('Some unexpected error during DB creation:"\n' + traceback.format_exc())
                return False

    def check_sales_table(self):
        """
        Check if "Sales" table is available, if not calls create_sales_table().
        :return: In case of success returns True, in case of any problem False.
        """
        try:
            self.logger.info('Sales table check start.')
            sql = 'SELECT COUNT(*) FROM information_schema.tables WHERE table_name="sales"'
            db_cursor = self.db_connection.cursor()
            db_cursor.execute(sql)
            if db_cursor.fetchone()[0] == 1:
                db_cursor.close()
                self.logger.info("Sales table is in place.")
                return True
            else:
                if self.create_sales_table():
                    db_cursor.close()
                    return True
                else:
                    self.db_connection.close()
                    return False
        except mysql.connector.Error:
            self.logger.error('Some unexpected error during Sales table check:"\n' + traceback.format_exc())
            return False

    def create_sales_table(self):
        """
        Creates sales table.
        :return: In case of success returns True, in case of any problem False.
        """
        try:
            sql = 'CREATE TABLE `sales` ' \
                  '(`seller_name` VARCHAR(40) NOT NULL,`number_of_sales` INT NOT NULL,' \
                  '`total_value` DOUBLE NOT NULL,PRIMARY KEY (`seller_name`));'
            db_cursor = self.db_connection.cursor()
            db_cursor.execute(sql)
            db_cursor.close()
            self.db_connection.commit()
            self.logger.info('Sales table created.')
            return True
        except mysql.connector.Error:
            self.logger.error('Some unexpected error during Sales table creation:"\n' + traceback.format_exc())
            return False

    def close_db_connection(self):
        """
        Close connection to MySQL.
        :return:
        """
        self.db_connection.close()
        self.logger.info('DB connection closed.')
        return

    def create_db_schema(self, db_name):
        """
        Creates DB.
        :return: In case of success returns True, in case of any problem False.
        """
        try:
            db_cursor = self.db_connection.cursor()
            db_cursor.execute('CREATE SCHEMA ' + db_name)
            db_cursor.close()
            return True
        except mysql.connector.Error:
            self.logger.error('Error during DB schema creation:"\n' + traceback.format_exc())
            db_cursor.close()
            return False

    def get_data_from_sales_table(self):
        """
        Get all data from "Sales" table.
        :return: retrieved data
        """
        try:
            db_cursor = self.db_connection.cursor()
            db_cursor.execute('SELECT * FROM `sales` ORDER BY `sales`.`seller_name`')
            result = db_cursor.fetchall()
            db_cursor.close()
            return result
        except mysql.connector.Error:
            self.logger.error('Problems during getting Sales table data:"\n' + traceback.format_exc())
            return None

    def add_empty_seller_to_db(self, seller_name):
        """
        Adds empty seller record.
        :param seller_name:
        :return:  In case of success returns True, in case of any problem False.
        """
        try:
            sql = 'INSERT INTO `sales` (`seller_name`,' \
                  ' `number_of_sales`, `total_value`) VALUES (\'' + seller_name + '\', \'0\', \'0\')'
            db_cursor = self.db_connection.cursor()
            db_cursor.execute(sql)
            db_cursor.close()
            self.db_connection.commit()
            self.logger.info('Seller ' + seller_name + ' empty data added to DB.')
            return True
        except mysql.connector.Error:
            self.logger.error('Error during empty seller adding to DB:"\n' + traceback.format_exc())
            return False

    def check_seller_existence(self, seller_name):
        """
        Check if seller record exists in "Sales" table, if not calls add_empty_seller_to_db().
        :param seller_name:
        :return: In case of success returns True, in case of any problem False.
        """
        try:
            sql = 'SELECT COUNT(*) FROM sales WHERE `sales`.`seller_name`="' + seller_name + '"'
            db_cursor = self.db_connection.cursor()
            db_cursor.execute(sql)
            record_number = db_cursor.fetchone()[0]
            db_cursor.close()
            if record_number == 1:
                self.logger.info('User with name - ' + seller_name + ' exists, no need in new record creation.')
            else:
                self.logger.info('Adding user - ' + seller_name + ' to DB.')
                if not self.add_empty_seller_to_db(seller_name):
                    return False
            return True
        except mysql.connector.Error:
            self.logger.error('Some problems during user existence check:"\n' + traceback.format_exc())
            db_cursor.close()
            return False

    def update_seller_sale_statistics(self, seller_name, value, count=1):
        """
        Updates seller sale statistics in "Sales" table.
        :param seller_name:
        :param value: sale total value
        :param count: sales count, default 1
        :return: In case of success returns True, in case of any problem False.
        """
        try:
            sql = 'UPDATE `sales` SET `number_of_sales` = `number_of_sales` + ' + str(count) + ', ' \
                    '`total_value` = `total_value` + ' + str(value) + ' ' \
                    'WHERE `seller_name`="' + seller_name + '"'
            db_cursor = self.db_connection.cursor()
            db_cursor.execute(sql)
            db_cursor.close()
            self.db_connection.commit()
            return True
        except mysql.connector.Error:
            self.logger.error('Unexpected error during Sales table update:\n' + traceback.format_exc())
            return False

    def prepare_db_connection(self):
        """
        Opens DB connection and calls check_db(), check_sales_table().
        :return: In case of success returns True, in case of any problem False.
        """
        if not self.open_db_connection():
            self.logger.error('No DB connection is established.')
            return False
        if not self.check_db():
            self.logger.error('Problems during DB check, please check log.')
            print('Problems during DB check, please check log.\nApplication will exit now.')
            return False
        if not self.check_sales_table():
            self.logger.error('Problems with Sales table, please check log.')
            return False
        return True

