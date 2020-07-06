from modulos.usuario.repository import UsuarioRepository
from modulos.dbMysql import MysqlDB
from modulos.configuration import MySQLConfig


def main():
    config = MySQLConfig()
    mysql_db = MysqlDB(config)
    usuario_repository = UsuarioRepository(mysql_db)

    rodrigo = usuario_repository.find_by_id(1)

    print(rodrigo)

    rodrigo['password'] = '123'

    usuario_repository.delete(rodrigo)

    usuarios = usuario_repository.find_all()

    for usuario in usuarios:
        print(usuario['id'])


if __name__ == '__main__':
    main()
