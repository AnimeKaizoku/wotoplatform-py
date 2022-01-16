
import json
import socket
import threading
from wotoplatform.types.errors.serverErrors import WrongUsername
from wotoplatform.types.usersData import(
    LoginUserData, 
    LoginUserResult,
    RegisterUserResponse, 
    RegisterUserResult,
)

from wotoplatform.types.versionData import VersionResponse
from .tools import (
    make_sure_num,
    make_sure_byte, 
)
from .types.errors import (
    ClientException,
    InvalidTypeException,
    ClientVersionNotAcceptable,
    ClientNotInitializedException,
    ClientAlreadyInitializedException,
)
from .types import (
    ClientBase,
    DScaffold,
    RScaffold,
    Scaffold,
    VersionData,
    RegisterUserData,
)


__version__ = '0.0.10'


class WotoClient(ClientBase):
    username: str = ''
    password: str = ''
    endpoint_url: str = ''
    auth_key: str = ''
    access_hash: str = ''
    is_initialized: bool = False
    is_logged_in: bool = False
    client_version: VersionData = None
    __woto_socket: socket.socket = None
    __MAX_DATA_COUNTER = 8

    client_lock = threading.Lock()

    def __init__(
        self, 
        username: str, 
        password: str, 
        endpoint: str = 'wotoplatform.hakai.animekaizoku.com', 
        port: int = 50100,
    ):
        self.username = username
        self.password = password

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((endpoint, port))
        self.__woto_socket = s
    
    def start(self) -> None:
        if self.is_initialized:
            raise ClientAlreadyInitializedException()
        
        self.client_version = VersionData()
        self.is_initialized = True
        try:
            version_response = self.send_and_parse(self.client_version)
            if not isinstance(version_response, VersionResponse):
                raise InvalidTypeException(VersionResponse, type(version_response))
            
            if not version_response.success:
                raise version_response.get_exception()
            
            if not version_response.result.is_acceptable:
                raise ClientVersionNotAcceptable()
        
            try:
                self._login(
                    username=self.username,
                    password=self.password,
                    auth_key=self.auth_key,
                    access_hash=self.access_hash,
                )
            except WrongUsername:
                self._register(
                    username=self.username,
                    password=self.password,
                )
            
        except:
            self.is_initialized = False
            raise

    
    def _login(self, username: str, password: str, auth_key:str, access_hash: str) -> LoginUserResult:
        """
        Login user. Don't use this method directly, instead use start method.
        """
        response = self.send_and_parse(
            LoginUserData(
                username=username,
                password=password,
                auth_key=auth_key,
                access_hash=access_hash,
            )
        )

        if not response.success:
            raise response.get_exception()
        
        return response.result

    def _register(self, username: str, password: str) -> RegisterUserResult:
        """
        Registers a new user on woto-platform. 
        Don't use this method directly, instead use start method.
        """
        response = self.send_and_parse(
            RegisterUserData(
                username=username,
                password=password,
            )
        )
        
        if not isinstance(response, RegisterUserResponse):
            raise InvalidTypeException(RegisterUserResponse, type(response))

        if not response.success:
            raise response.get_exception()
        

        return response.result

    def _write_data(self, data: bytes):
        bb = make_sure_num(len(data), self.__MAX_DATA_COUNTER)
        bb = make_sure_byte(bb, self.__MAX_DATA_COUNTER)
        self.__woto_socket.send(bb + data)
    
    def _read_data(self) -> bytes:
        count = self.__woto_socket.recv(self.__MAX_DATA_COUNTER)
        count = int(count.decode('utf-8').strip())
        return self.__woto_socket.recv(count)
    
    def send(self, scaffold: Scaffold) -> bytes:
        if not self.is_initialized:
            raise ClientNotInitializedException()
        
        if not isinstance(scaffold, Scaffold):
            raise InvalidTypeException(Scaffold, type(scaffold))

        with self.client_lock:
            self._write_data(scaffold.get_as_bytes())
            return self._read_data()
    
    def send_and_parse(self, scaffold: DScaffold) -> RScaffold:
        if not isinstance(scaffold, DScaffold):
            return None
        
        response_type = scaffold.get_response_type()
        if not response_type:
            return None
        
        return response_type(**json.loads(self.send(scaffold)))



client = WotoClient(
    username='aliwoto', 
    password='12345678910', 
    endpoint='localhost',
    port=50100,
)

client.start()



