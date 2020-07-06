from os import environ


class MySQLConfig:

    def __init__(self):
        self.__host = environ['DB_HOST']
        self.__username = environ['DB_USERNAME']
        self.__password = environ['DB_PWD']
        self.__database = environ['DB_NAME']

    def getHost(self):
        return self.__host

    def getUsername(self):
        return self.__username

    def getPassword(self):
        return self.__password

    def getDatabase(self):
        return self.__database
