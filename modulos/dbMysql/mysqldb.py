from mysql import connector
from modulos.configuration.mysql import MySQLConfig

config = MySQLConfig()


class MysqlDB:

    def __init__(self):
        self.__db = connector.connect(host=config.getHost(), user=config.getUsername(), passwd=config.getPassword(),
                                      database=config.getDatabase())
        self.__cursor = self.__db.cursor()

    def executeSelect(self, query, params):
        return self.__cursor.execute(query, params)

    def executeUpdate(self, query, params):
        self.__cursor.execute(query, params)
        self.__db.commit()

    def executeDDL(self, query):
        self.__cursor.execute(query)
