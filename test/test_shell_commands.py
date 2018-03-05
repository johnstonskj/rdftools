from rdftools.scripts import shell

def test_commands_added():
    for cmd in ['base', 'help', 'exit']:
        assert cmd in shell.COMMANDS

def test_command_help():
    pass

def test_command_completion():
    pass
