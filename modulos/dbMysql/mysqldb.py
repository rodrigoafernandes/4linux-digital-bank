from mysql import connector
from modulos.configuration.mysql import MySQLConfig

config = MySQLConfig()


class MysqlDB:

    def __init__(self):
        self.__db = connector.connect(host=config.getHost(), user=config.getUsername(), passwd=config.getPassword(),
                                      database=config.getDatabase())
        self.__cursor = self.__db.cursor()

    def executeSelectParams(self, query, params):
        return self.__cursor.execute(query, params)

    def executeSelect(self, query):
        return self.__cursor.execute(query)

    def executeUpdateDelete(self, query, params):
        self.__cursor.execute(query, params)
        self.__db.commit()

    def executeInsert(self, query, params):
        self.__cursor.execute(query, params)
        self.__db.commit()
        return self.__cursor.lastrowid

    def executeDDL(self, query):
        self.__cursor.execute(query)
