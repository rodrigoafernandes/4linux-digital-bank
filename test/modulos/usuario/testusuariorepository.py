from mockito import mock, unstub, verify, when
from unittest import TestCase, main
from modulos.usuario.exceptions.UsuarioJaCadastradoException import UsuarioJaCadastrado
from modulos.usuario.exceptions.usuarionotfoundexception import UsuarioNotFound
from modulos.usuario.repository.usuariorepository import UsuarioRepository
from modulos.usuario.repository.usuarioqueries import (
    query_delete, query_find_all, query_find_by_id, query_find_by_login, query_insert, query_update
)
from modulos.dbMysql.mysqldb import MysqlDB


class TestUsuarioRepository(TestCase):

    def __init__(self, *args, **kwargs):
        super(TestUsuarioRepository, self).__init__(*args, **kwargs)

    def test_givenUsuarioFound_whenSearchUsuarioById_thenShouldReturnsDicUsuario(self):
        self.__setUpTableExists()
        id_usuario = 1
        when(self.__mysql_db).executeSelectParams(query_find_by_id, (id_usuario,)).thenReturn([(1, 'Usuario Teste',
                                                                                                'rodrigo', 'senha123',
                                                                                                1)])
        usuario = self.__usuario_repository.findById(id_usuario)

        self.assertEqual(id_usuario, usuario['id'])

        unstub()

    def test_givenUsuarioNotFound_whenSearchUsuarioById_thenShouldRaisesUsuarioNotFound(self):
        id_usuario = 0
        self.__setUpTableExists()
        when(self.__mysql_db).executeSelectParams(query_find_by_id, (id_usuario,)).thenReturn([])

        with self.assertRaises(UsuarioNotFound):
            self.__usuario_repository.findById(id_usuario)

        unstub()

    def test_givenUsuarioFound_whenSearchUsuarioByLogin_thenShouldReturnsDicUsuario(self):
        self.__setUpTableExists()

        expected_id_usuario = 1
        login = 'rodrigo'
        when(self.__mysql_db).executeSelectParams(query_find_by_login, (login, )).thenReturn([(1, 'Usuario Teste',
                                                                                               'rodrigo', 'senha123',
                                                                                               1)])
        usuario = self.__usuario_repository.findByLogin(login)
        self.assertEqual(expected_id_usuario, usuario['id'])

        unstub()

    def test_givenUsuarioNotFound_whenSearchUsuarioByLogin_thenShouldRaisesUsuarioNotFound(self):
        self.__setUpTableExists()

        login = 'rodrigo132'
        when(self.__mysql_db).executeSelectParams(query_find_by_login, (login, )).thenReturn([])

        with self.assertRaises(UsuarioNotFound):
            self.__usuario_repository.findByLogin(login)

        unstub()

    def test_givenUsuariosFound_whenSearchAllUsuarios_thenShouldReturnsListOfDicUsuario(self):
        self.__setUpTableExists()

        when(self.__mysql_db).executeSelect(query_find_all).thenReturn([(1, 'Usuario Teste', 'rodrigo', 'senha123', 1)])
        usuarios = self.__usuario_repository.findAll()
        self.assertEqual(1, len(usuarios))

        unstub()

    def test_givenUsuariosNotFound_whenSearchAllUsuarios_thenShouldRaisesUsuarioNotFound(self):
        self.__setUpTableExists()

        when(self.__mysql_db).executeSelect(query_find_all).thenReturn([])

        with self.assertRaises(UsuarioNotFound):
            self.__usuario_repository.findAll()

        unstub()

    def test_givenUsuarioFound_whenSaveNewUsuario_thenShouldRaisesUsuarioJaCadastrado(self):
        self.__setUpTableExists()

        usuario = {'nome': "Teste", 'login': 'test', 'password': '132', 'admin': 0}
        when(self.__mysql_db).executeSelectParams(query_find_by_login, (usuario['login'],)).thenReturn([
            (1, 'Usuario Teste', 'test', 'senha123', 1)])

        with self.assertRaises(UsuarioJaCadastrado):
            self.__usuario_repository.save(usuario)

        unstub()

    def test_givenUsuarioNotFound_whenSaveNewUsuario_thenShouldReturnsDicUsuarioWithGeneratedId(self):
        self.__setUpTableExists()

        usuario = {'nome': "Teste", 'login': 'test', 'password': '132', 'admin': 0}
        when(self.__mysql_db).executeSelectParams(query_find_by_login, (usuario['login'],)).thenReturn([])
        when(self.__mysql_db).executeInsert(query_insert, (usuario['nome'], usuario['login'], usuario['password'],
                                                           usuario['admin'])).thenReturn(2)

        new_usuario = self.__usuario_repository.save(usuario)
        self.assertEqual(2, new_usuario['id'])

        unstub()

    def test_givenUsuarioNotFound_whenDeleteUsuario_thenShouldRaisesUsuarioNotFound(self):
        self.__setUpTableExists()

        usuario = {'id': 1, 'nome': "Teste", 'login': 'test', 'password': '132', 'admin': 0}
        when(self.__mysql_db).executeSelectParams(query_find_by_id, (usuario['id'],)).thenReturn([])

        with self.assertRaises(UsuarioNotFound):
            self.__usuario_repository.delete(usuario)

        unstub()

    def test_givenUsuarioFound_whenDeleteUsuario_thenShouldDeleteUsuario(self):
        self.__setUpTableExists()

        usuario = {'id': 1, 'nome': "Teste123", 'login': 'test', 'password': '132', 'admin': 0}
        when(self.__mysql_db).executeSelectParams(query_find_by_id, (usuario['id'],)).thenReturn([(1, 'Teste', 'test',
                                                                                                   '321', 0), ])
        when(self.__mysql_db).executeUpdateDelete(query_delete, (usuario['id'])).thenReturn(1)

        self.__usuario_repository.delete(usuario)

        verify(self.__mysql_db, times=1).executeUpdateDelete(query_delete, (usuario['id']))

        unstub()

    def test_givenUsuarioNotFound_whenUpdateUsuario_thenShouldRaisesUsuarioNotFound(self):
        self.__setUpTableExists()

        usuario = {'id': 1, 'nome': "Teste", 'login': 'test', 'password': '132', 'admin': 0}
        when(self.__mysql_db).executeSelectParams(query_find_by_id, (usuario['id'],)).thenReturn([])

        with self.assertRaises(UsuarioNotFound):
            self.__usuario_repository.update(usuario)

        unstub()

    def test_givenUsuarioFound_whenUpdateUsuario_thenShouldUpdateUsuario(self):
        self.__setUpTableExists()

        usuario = {'id': 1, 'nome': "Teste123", 'login': 'test', 'password': '132', 'admin': 0}
        when(self.__mysql_db).executeSelectParams(query_find_by_id, (usuario['id'],)).thenReturn([(1, 'Teste', 'test',
                                                                                                   '321', 0), ])
        when(self.__mysql_db).executeUpdateDelete(query_update, (usuario['nome'], usuario['password'], usuario['admin'],
                                                                 usuario['id'])).thenReturn(1)

        self.__usuario_repository.update(usuario)

        verify(self.__mysql_db, times=1).executeUpdateDelete(query_update, (usuario['nome'], usuario['password'],
                                                                            usuario['admin'], usuario['id']))

        unstub()

    def test_givenTableUsuarioNotFound_whenCreateNewUsuarioRepository_thenShouldCreateTable(self):
        self.__setUpTableNotExists()
        verify(self.__mysql_db, times=1).executeDDL(self.__command)
        unstub()

    def __setUpTableExists(self):
        self.__mysql_db = mock(MysqlDB)
        self.__tables = [('Usuario', ), ]
        when(self.__mysql_db).executeSelect('SHOW TABLES').thenReturn(self.__tables)
        self.__usuario_repository = UsuarioRepository(self.__mysql_db)

    def __setUpTableNotExists(self):
        self.__mysql_db = mock(MysqlDB)
        self.__tables = [('Teste', ), ]
        self.__command = 'CREATE TABLE Usuario (id INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(50) CHARACTER SET utf8, login VARCHAR(10) CHARACTER SET utf8, password VARCHAR(10) CHARACTER SET utf8, admin TINYINT(1) DEFAULT 0)'
        when(self.__mysql_db).executeSelect('SHOW TABLES').thenReturn(self.__tables)
        when(self.__mysql_db).executeDDL(self.__command).thenReturn(1)
        self.__usuario_repository = UsuarioRepository(self.__mysql_db)

    def __exit__(self, exc_type, exc_val, exc_tb):
        unstub()


if __name__ == '__main__':
    main()
