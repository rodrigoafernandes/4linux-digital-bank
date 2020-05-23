from .usuarioqueries import query_find_by_id, query_find_by_login, query_find_all, query_insert, query_update, \
    query_delete
from data.usuariosqlfile import getSqlCommandsUsuario
from modulos.dbMysql.mysqldb import MysqlDB
from modulos.usuario.exceptions.usuarionotfoundexception import UsuarioNotFound
from modulos.usuario.exceptions.UsuarioJaCadastradoException import UsuarioJaCadastrado

mysqlDB = MysqlDB()


class UsuarioRepository:

    def __init__(self):
        self.__exists = False
        self.__validaTabelaUsuario()

    def findById(self, iDUsuario):
        result = mysqlDB.executeSelectParams(query_find_by_id, (iDUsuario,))
        if len(result) < 1:
            raise UsuarioNotFound(f'Não existe usuário com o id: {iDUsuario}')

        return self.__convertToUsuarioDic(result[0])

    def findByLogin(self, login):
        result = mysqlDB.executeSelectParams(query_find_by_login, (login,))

        if len(result) < 1:
            raise UsuarioNotFound(f'Não há usuários cadastrados com o login: {login}')

        return self.__convertToUsuarioDic(result[0])

    def findAll(self):
        usuarios = []
        result = mysqlDB.executeSelectParams(query_find_all)

        if len(result) < 1:
            raise UsuarioNotFound('Não há usuários cadastrados,')

        for usuario in result:
            usuarios.append(self.__convertToUsuarioDic(usuario))

        return usuarios

    def save(self, usuario):
        try:
            self.findByLogin(usuario['login'])
        except UsuarioNotFound:
            iduser = mysqlDB.executeInsert(query_insert, (usuario['nome'], usuario['login'], usuario['password'],
                                                          usuario['admin']))
            usuario['id'] = iduser

            return usuario
        else:
            raise UsuarioJaCadastrado(f'Login: {usuario["login"]} já cadastrado')

    def update(self, usuario):
        self.findById(usuario['id'])
        mysqlDB.executeUpdateDelete(query_update,
                                    (usuario['nome'], usuario['password'], usuario['admin'], usuario['id']))

    def delete(self, usuario):
        self.findById(usuario['id'])
        mysqlDB.executeUpdateDelete(query_delete, (usuario['id']))

    def __validaTabelaUsuario(self):
        if not self.__exists:
            tables = mysqlDB.executeSelectParams('SHOW TABLES')

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
