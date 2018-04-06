import db_utils
import logging

logger = logging.getLogger('CoffeeForMe_application')
logger.setLevel(logging.DEBUG)
logFile = logging.FileHandler('all.log')
logFile.setLevel(logging.DEBUG)

logFormatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logFile.setFormatter(logFormatter)

logger.addHandler(logFile)

userName = ''
role = ''

userName = input('Welcome to CoffeeForMe seller/manager system!'
                 '\nInput your user name: ')
logger.info('User name is: ' + userName)
role = input('Input your role(seller/manager): ')
if role == 'seller':
    print('You are in seller mode.')
    connection = db_utils.open_db_connection()
    db_utils.close_db_connection(connection)
elif role == 'manager':
    print('You are in manager mode.')
else :
    print('Role is wrong!')
