from modulos.configuration.mysql.config import MySQLConfig
from unittest import TestCase, main
from os import environ

dbHost = 'localhost'
dbUser = 'test'
dbPassword = 'test123'
dbName = '4LDBKTST01'


class TestMysqlConfig(TestCase):
    def test_GivenEnvironmentVariablesFound_WhenCreateMySqlConfigObj_thenShouldReturnsNewObj(self):
        self.__setEnviron()

        mysqlConfig = MySQLConfig()

        self.assertEqual(dbHost, mysqlConfig.getHost())
        self.assertEqual(dbUser, mysqlConfig.getUsername())
        self.assertEqual(dbPassword, mysqlConfig.getPassword())
        self.assertEqual(dbName, mysqlConfig.getDatabase())

        self.__clearEnviron()

    def test_GivenEnvironmentVariablesNotFound_WhenCreateMySqlConfigObj_thenShoulRaiseKeyError(self):
        with self.assertRaises(KeyError):
            mysqlConfig = MySQLConfig()

    def __setEnviron(self):
        environ['DB_HOST'] = dbHost
        environ['DB_USERNAME'] = dbUser
        environ['DB_PWD'] = dbPassword
        environ['DB_NAME'] = dbName

    def __clearEnviron(self):
        environ.clear()


if __name__ == '__main__':
    main()
