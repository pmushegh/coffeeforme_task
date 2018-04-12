from classes import employee

import logging

logger = logging.getLogger(__name__)


class Manager(employee.Employee):
    def __init__(self, name):
        super().__init__(name, 'manager')

    def interactions_silent(self, db_connection, args=None):
        self.interactions(db_connection)

    def interactions(self, db_connection):
        print('You are in manager mode.')
        logger.info('Getting sale data.')
        all_sale_data = db_connection.get_data_from_sales_table()
        if all_sale_data is None:
            print('Problems with getting sales data.'
                  '\nApplication will exit now.')
            logger.error('Unable to retrieve sale data.')
        else:
            logger.info('Printing sales data.')
            total_sales_value = 0.0
            print('|' + '-' * 82 + '|')
            print('|Sales data:' + ' ' * 71 + '|')
            print('|' + '-' * 82 + '|')
            print('|{0:40}|{1:20}|{2:20}|'.format('Seller name', 'Number of sales', 'Total Value ($)'))
            print('|' + '-' * 82 + '|')
            for seller_name, sales_num, total_value in all_sale_data:
                total_sales_value += total_value
                print('|{0:40}|{1:<20d}|{2:<20}|'.format(seller_name, sales_num, total_value))
                print('|' + '-' * 82 + '|')
            print('|' + ' ' * 40 + '|' + ' ' * 20 + '|{0:20}|'.format('Total:' + str(total_sales_value)))
            print('|' + '-' * 82 + '|')
            logger.info('Finished printing sale data.')
        return
