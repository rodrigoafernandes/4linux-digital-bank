query_find_by_id = """ SELECT usuario.id, usuario.nome, usuario.login, usuario.password, usuario.admin 
FROM Usuario usuario WHERE usuario.id = %s
"""

query_find_by_login = """SELECT usuario.id, usuario.nome, usuario.login, usuario.password, usuario.admin 
FROM Usuario usuario WHERE usuario.login = %s"
"""

query_find_all = """SELECT usuario.id, usuario.nome, usuario.login, usuario.password, usuario.admin 
FROM Usuario usuario
"""

query_insert = """INSERT INTO Usuario (nome, login, password, admin) VALUES (%s, %s, %s, %s)"""

query_update = """UPDATE Usuario SET nome=%s, password=%s, admin=%s WHERE id=%s"""

query_delete = """DELETE FROM Usuario usuario WHERE usuario.id=%s
"""