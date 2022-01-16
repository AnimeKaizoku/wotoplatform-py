import json
import threading
from typing import Union

from wotoplatform.types.usersData import(
    GetMeData, GetMeResult, GetUserInfoResult, ResolveUsernameResult
)
from .utils import (
    WotoSocket,
)
from .tools import (
    make_sure_byte, 
)
from .types.errors import (
    WrongUsername,
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
    VersionResponse,
    RegisterUserData,
    LoginUserData, 
    LoginUserResult,
    RegisterUserResponse, 
    RegisterUserResult,
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
    __woto_socket: WotoSocket = None
    __MAX_DATA_COUNTER = 8

    client_lock = threading.Lock()

    def __init__(
        self, 
        username: str, 
        password: str, 
        endpoint: str = 'wotoplatform.hakai.animekaizoku.com', 
        port: int = 50100,
    ):
        if not username:
            raise ValueError('username cannot be empty')
        if not password:
            raise ValueError('password cannot be empty')
        
        self.username = username
        self.password = password

        self.__woto_socket = WotoSocket(host=endpoint, port=port)
    
    async def start(self) -> None:
        if self.is_initialized:
            raise ClientAlreadyInitializedException()
        
        if not self.__woto_socket.is_initialized:
            await self.__woto_socket.connect()
        
        self.client_version = VersionData()
        self.is_initialized = True
        try:
            version_response = await self.send_and_parse(self.client_version)
            if not isinstance(version_response, VersionResponse):
                raise InvalidTypeException(VersionResponse, type(version_response))
            
            if not version_response.success:
                raise version_response.get_exception()
            
            if not version_response.result.is_acceptable:
                raise ClientVersionNotAcceptable()
        
            try:
                await self._login(
                    username=self.username,
                    password=self.password,
                    auth_key=self.auth_key,
                    access_hash=self.access_hash,
                )
            except WrongUsername:
                await self._register(
                    username=self.username,
                    password=self.password,
                )
            
        except:
            self.is_initialized = False
            raise

    
    async def _login(self, username: str, password: str, auth_key:str, access_hash: str) -> LoginUserResult:
        """
        Login user. Don't use this method directly, instead use start method.
        """
        response = await self.send_and_parse(
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

    async def _register(self, username: str, password: str) -> RegisterUserResult:
        """
        Registers a new user on woto-platform. 
        Don't use this method directly, instead use start method.
        """
        response = await self.send_and_parse(
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

    async def _write_data(self, data: bytes):
        bb = str(len(data)).zfill(self.__MAX_DATA_COUNTER)
        bb = make_sure_byte(bb, self.__MAX_DATA_COUNTER)
        await self.__woto_socket.send(bb + data)
    
    async def _read_data(self) -> bytes:
        count = await self.__woto_socket.recv(self.__MAX_DATA_COUNTER)
        count = int(count.decode('utf-8').strip())
        return await self.__woto_socket.recv(count)
    
    async def send(self, scaffold: Scaffold) -> bytes:
        if not self.is_initialized:
            raise ClientNotInitializedException()
        
        if not isinstance(scaffold, Scaffold):
            raise InvalidTypeException(Scaffold, type(scaffold))

        with self.client_lock:
            await self._write_data(scaffold.get_as_bytes())
            return await self._read_data()
    
    async def send_and_parse(self, scaffold: DScaffold) -> RScaffold:
        if not isinstance(scaffold, DScaffold):
            return None
        
        response_type = scaffold.get_response_type()
        if not response_type:
            return None
        
        return response_type(**json.loads(await self.send(scaffold)))

    async def get_me(self) -> GetMeResult:
        response = await self.send_and_parse(GetMeData())

        if not response.success:
            raise response.get_exception()
        
        return response.result

    async def get_user_info(self, user_id: Union[int, str]) -> GetUserInfoResult:
        pass

    async def resolve_username(self, username: str) -> ResolveUsernameResult:
        pass


    async def get_group_call_info(self):
        pass
    
    async def create_group_call(self):
        pass


    async def delete_group_call(self):
        pass

    async def get_group_call_queue(self):
        pass

    async def get_group_call_history(self):
        pass

    async def add_to_queue(self):
        pass


    async def create_new_media(self):
        pass

    
    



