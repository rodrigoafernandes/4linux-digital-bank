import pathlib


def getSqlCommandsUsuario():
    with open(f'{pathlib.Path(__file__).parent.absolute()}/CREATE_TABLE_Usuario.txt', 'r') as arquivo:
        conteudo = arquivo.readlines()
        return conteudo
