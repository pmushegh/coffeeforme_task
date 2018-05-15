from abc import ABCMeta, abstractmethod


class Employee(metaclass=ABCMeta):
    """
    Employee class.
    """
    def __init__(self, name, role):
        self.name = name
        self.role = role

    @abstractmethod
    def interactions(self, db_connection):
        """
        Employee interaction base on commandline arguments.
        Should be override in child class, have no logic.
        :param db_connection: DBUtils type object
        :param args: commandline arguments
        :return:
        """
        pass

    @abstractmethod
    def interactions_silent(self, db_connection, args):
        """
        Employee interaction base on commandline arguments.
        Should be override in child class, have no logic.
        :param db_connection: DBUtils type object
        :param args: commandline arguments
        :return:
        """
        pass

