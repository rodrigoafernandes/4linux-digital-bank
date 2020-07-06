from mockito import mock, unstub, verify, when
from mysql import connector
from mysql.connector.fabric.connection import MySQLCursor, MySQLFabricConnection
from unittest import TestCase, main
from modulos.dbMysql.mysqldb import MysqlDB
from modulos.configuration.mysql.config import MySQLConfig


class TestMysqlDB(TestCase):

    def __init__(self, *args, **kwargs):
        super(TestMysqlDB, self).__init__(*args, **kwargs)
        self.__setUp()

    def test_givenSelectQuerySuccessfullyExecuted_whenExecuteSelect_thenShouldReturnsListOfDic(self):
        query = 'SELECT * FROM Teste t'
        expected_result = [{'id': 1, 'atr': 'Nome'}]

        when(self.__cursor).execute(query).thenReturn(True)
        when(self.__cursor).fetchall().thenReturn(expected_result)

        results = self.__mysqlDb.executeSelect(query)

        self.assertEqual(len(expected_result), len(results))
        self.assertEqual(expected_result[0]['id'], 1)

    def test_givenSelectQueryWithParamsSuccessfullyExecuted_whenExecuteSelectWithParams_thenShouldReturnsListOfDic(self):
        search_id = 1
        query = 'SELECT * FROM Teste t WHERE t.id = %s'
        params = (search_id,)
        expected_result = [{'id': 1, 'atr': 'Nome'}]

        when(self.__cursor).execute(query, params).thenReturn(True)
        when(self.__cursor).fetchall().thenReturn(expected_result)

        results = self.__mysqlDb.executeSelectParams(query, params)

        self.assertEqual(len(expected_result), len(results))
        self.assertEqual(expected_result[0]['id'], 1)

    def test_givenUpdateQuery_whenExecuteUpdateOrDelete_thenShouldCallsDBOnlyOneTime(self):
        search_id = 1
        new_value = 'Nome 132'
        query = 'UPDATE Teste set atr = %s WHERE id = %s'
        params = (new_value, search_id, )
        expected_result = []

        when(self.__cursor).execute(query, params).thenReturn(expected_result)
        when(self.__db).commit().thenReturn(1)

        self.__mysqlDb.executeUpdateDelete(query, params)

        verify(self.__db, times=1).commit()

    def test_givenInsertQuery_whenExecuteInsert_thenShouldReturnsTheIdGenerated(self):
        new_id_expected = 2
        query = 'INSERT INTO Teste(atr) VALUES(%s)'
        params = ('Nome 456', )
        expected_result = []

        when(self.__cursor).execute(query, params).thenReturn(expected_result)
        when(self.__db).commit().thenReturn(1)

        id_generated = self.__mysqlDb.executeInsert(query, params)

        self.assertEqual(new_id_expected, id_generated)

    def test_givenDDLQuery_whenExecuteDDL_thenShouldCallsDBOnlyOneTime(self):
        query = 'CREATE TABLE Teste (id INT AUTO_INCREMENT PRIMARY KEY, atr VARCHAR(50) CHARACTER SET utf8)'
        expected_result = []

        when(self.__cursor).execute(query).thenReturn(expected_result)

        self.__mysqlDb.executeDDL(query)

        verify(self.__cursor, times=1).execute(query)

    def __setUp(self):
        self.__dbHost = 'localhost'
        self.__dbUser = 'test'
        self.__dbPassword = 'test123'
        self.__dbName = '4LDBKTST01'
        self.__config = mock(MySQLConfig)
        self.__db = mock(MySQLFabricConnection)
        self.__cursor = mock({
            'lastrowid': 2
        }, spec=MySQLCursor)
        when(self.__config).getHost().thenReturn(self.__dbHost)
        when(self.__config).getUsername().thenReturn(self.__dbUser)
        when(self.__config).getPassword().thenReturn(self.__dbPassword)
        when(self.__config).getDatabase().thenReturn(self.__dbName)
        when(connector).connect(host=self.__dbHost, user=self.__dbUser, passwd=self.__dbPassword,
                                database=self.__dbName).thenReturn(self.__db)
        when(self.__db).cursor().thenReturn(self.__cursor)
        self.__mysqlDb = MysqlDB(self.__config)

    def __exit__(self, exc_type, exc_val, exc_tb):
        unstub()


if __name__ == '__main__':
    main()
