from .usuarioqueries import query_find_by_id, query_find_by_login, query_find_all, query_insert, query_update, \
    query_delete
from data.usuariosqlfile import getSqlCommandsUsuario
from modulos.usuario.exceptions.usuarionotfoundexception import UsuarioNotFound
from modulos.usuario.exceptions.UsuarioJaCadastradoException import UsuarioJaCadastrado


class UsuarioRepository:

    def __init__(self, mysql_db):
        self.__mysqlDB = mysql_db
        self.__exists = False
        self.__valida_tabela_usuario()

    def find_by_id(self, id_usuario):
        result = self.__mysqlDB.executeSelectParams(query_find_by_id, (id_usuario,))
        if len(result) < 1:
            raise UsuarioNotFound(f'Não existe usuário com o id: {id_usuario}')

        return self.__convert_to_usuario_dic(result[0])

    def find_by_login(self, login):
        result = self.__mysqlDB.executeSelectParams(query_find_by_login, (login,))

        if len(result) < 1:
            raise UsuarioNotFound(f'Não há usuários cadastrados com o login: {login}')

        return self.__convert_to_usuario_dic(result[0])

    def find_all(self):
        usuarios = []
        result = self.__mysqlDB.executeSelect(query_find_all)

        if len(result) < 1:
            raise UsuarioNotFound('Não há usuários cadastrados,')

        for usuario in result:
            usuarios.append(self.__convert_to_usuario_dic(usuario))

        return usuarios

    def save(self, usuario):
        try:
            self.find_by_login(usuario['login'])
        except UsuarioNotFound:
            iduser = self.__mysqlDB.executeInsert(query_insert, (usuario['nome'], usuario['login'], usuario['password'],
                                                  usuario['admin']))
            usuario['id'] = iduser

            return usuario
        else:
            raise UsuarioJaCadastrado(f'Login: {usuario["login"]} já cadastrado')

    def update(self, usuario):
        self.find_by_id(usuario['id'])
        self.__mysqlDB.executeUpdateDelete(query_update,
                                           (usuario['nome'], usuario['password'], usuario['admin'], usuario['id']))

    def delete(self, usuario):
        self.find_by_id(usuario['id'])
        self.__mysqlDB.executeUpdateDelete(query_delete, (usuario['id'], ))

    def __valida_tabela_usuario(self):
        if not self.__exists:
            tables = self.__mysqlDB.executeSelect('SHOW TABLES')

            for table in tables:
                if 'Usuario' == table[0]:
                    self.__exists = True

            if not self.__exists:
                commands = getSqlCommandsUsuario()

                for command in commands:
                    self.__mysqlDB.executeDDL(command)

                self.__exists = True

    def __convert_to_usuario_dic(self, usuarioBD):
        return {'id': usuarioBD[0], 'nome': usuarioBD[1], 'login': usuarioBD[2], 'password': usuarioBD[3],
                'admin': usuarioBD[4]}
