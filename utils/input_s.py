import logging

from builtins import input


logger = logging.getLogger(__name__)


def input_s(message=''):
    """
    Reads value from console. In case of "exit" value throws UserWarning exception.
    :param message: input message for input() function
    :return: imputed value
    """
    temp = input(message)
    if temp == 'exit':
        print('Application will exit now.')
        logger.info('Exiting application after "exit" command.')
        raise UserWarning('Application exit on user demand.')
    return temp
