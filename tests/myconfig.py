import configparser

class ConfigForTest:
    username: str = ''
    password: str = ''
    host: str = ''
    port: int = 0
    
    def __init__(self):
        file = open('tests/config.ini', 'r')
        config = configparser.ConfigParser()
        config.read_file(file)

        self.username = config.get('main', 'username')
        self.password = config.get('main', 'password')
        self.host = config.get('main', 'host')
        self.port = config.getint('main', 'port')

the_config = ConfigForTest()
