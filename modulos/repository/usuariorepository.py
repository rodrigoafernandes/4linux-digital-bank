from data.usuariosqlfile import getSqlCommandsUsuario
from modulos.dbMysql.mysqldb import MysqlDB
from .exceptions.usuarionotfoundexception import UsuarioNotFound

mysqlDB = MysqlDB()


class UsuarioRepository:

    def __init__(self):
        self.__exists = False
        self.__validaTabelaUsuario()

    def findById(self, iDUsuario):
        result = mysqlDB.executeSelect("SELECT "
                                       "usuario.id, "
                                       "usuario.nome, "
                                       "usuario.login, "
                                       "usuario.password, "
                                       "usuario.admin "
                                       "FROM Usuario usuario "
                                       "WHERE usuario.id = %s", (iDUsuario,))
        if len(result) < 1:
            raise UsuarioNotFound(f'Não existe usuário com o id: {iDUsuario}')

        return self.__convertToUsuarioDic(result[0])

    def findByLogin(self, login):
        result = mysqlDB.executeSelect("SELECT "
                              "usuario.id, "
                              "usuario.nome, "
                              "usuario.login, "
                              "usuario.password, "
                              "usuario.admin "
                              "FROM Usuario usuario "
                              "WHERE usuario.login = %s", (login,))

        if len(result) < 1:
            raise UsuarioNotFound(f'Não há usuários cadastrados com o login: {login}')

        return self.__convertToUsuarioDic(result[0])

    def findAll(self):
        usuarios = []
        result = mysqlDB.executeSelect("SELECT "
                              "usuario.id, "
                              "usuario.nome, "
                              "usuario.login, "
                              "usuario.password, "
                              "usuario.admin "
                              "FROM Usuario usuario ")

        if len(result) < 1:
            raise UsuarioNotFound('Não há usuários cadastrados,')

        for usuario in result:
            usuarios.append(self.__convertToUsuarioDic(usuario))

        return usuarios

    def __validaTabelaUsuario(self):
        if not self.__exists:
            tables = mysqlDB.executeSelect("SHOW TABLES")

            for table in tables:
                if 'Usuario' == table[0]:
                    self.__exists = True

            if not self.__exists:
                commands = getSqlCommandsUsuario()

                for command in commands:
                    mysqlDB.executeDDL(command)

    def __convertToUsuarioDic(self, usuarioBD):
        return {'id': usuarioBD[0], 'nome': usuarioBD[1], 'login': usuarioBD[2], 'password': usuarioBD[3],
                'admin': usuarioBD[4]}
