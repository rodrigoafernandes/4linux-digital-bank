def getSqlCommandsUsuario():
    with open('CREATE_TABLE_Usuario.txt', 'r') as arquivo:
        conteudo = arquivo.readlines()
        return conteudo
