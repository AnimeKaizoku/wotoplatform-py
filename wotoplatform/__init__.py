
import json
import socket
import threading
from .tools import (
    make_sure_num,
    make_sure_byte, 
)

from .types.errors.general import (
    ClientException,
)
from .types.scaffold import (
    Scaffold,
)
from .types import (
    VersionData,
    VersionResponse,
)


__version__ = '0.0.10'


class WotoClient():
    username: str = ''
    password: str = ''
    endpoint_url: str = ''
    is_initialized: bool = False
    client_version: VersionData = None
    __woto_socket: socket.socket = None
    __MAX_DATA_COUNTER = 8

    client_lock = threading.Lock()

    def __init__(self, username: str, password: str, endpoint: str, port: int = 50100):

        self.username = username
        self.password = password

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((endpoint, port))
        self.__woto_socket = s
    
    def start(self) -> None:
        if self.is_initialized:
            raise ClientException('Client is already initialized.')
        
        self.client_version = VersionData()
        self.is_initialized = True
        try:
            print(VersionResponse(**json.loads(self.send(self.client_version))))
        except:
            self.is_initialized = False
            raise

        

    def _write_data(self, data: bytes):
        bb = make_sure_num(len(data), self.__MAX_DATA_COUNTER)
        bb = make_sure_byte(bb, self.__MAX_DATA_COUNTER)
        self.__woto_socket.send(bb + data)
    
    def _read_data(self) -> bytes:
        count = self.__woto_socket.recv(self.__MAX_DATA_COUNTER)
        count = int(count.decode('utf-8').strip())
        return self.__woto_socket.recv(count)
    
    def send(self, scaffold: Scaffold) -> bytes:
        if not scaffold:
            return None
        
        if not self.is_initialized:
            raise ClientException('Client is not initialized.')
        
        if not isinstance(scaffold, Scaffold):
            raise ClientException(f'Invalid type of data received: {type(scaffold)}.')

        with self.client_lock:
            self._write_data(scaffold.get_as_bytes())
            return self._read_data()



client = WotoClient(
    username='aliwoto', 
    password='1234567', 
    endpoint='localhost',
    port=50100,
)

client.start()



