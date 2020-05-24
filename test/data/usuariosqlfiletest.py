from unittest import TestCase, main

from data.usuariosqlfile import getSqlCommandsUsuario


class TestGetSqlCommands(TestCase):

    def test_GivenFileFound_whenGetSqlCommands_thenShouldReturnListOfString(self):
        qtcommands = 1
        commands = getSqlCommandsUsuario()
        self.assertEqual(qtcommands, len(commands))


if __name__ == '__main__':
    main()
