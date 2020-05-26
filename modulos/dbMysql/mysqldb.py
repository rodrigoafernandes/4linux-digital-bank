from mysql import connector


class MysqlDB:

    def __init__(self, config):
        self.__config = config
        self.__db = connector.connect(host=self.__config.getHost(), user=self.__config.getUsername(),
                                      passwd=self.__config.getPassword(), database=self.__config.getDatabase())
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
