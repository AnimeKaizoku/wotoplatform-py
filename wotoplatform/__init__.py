import json
import threading
from typing import Union

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
    GetUserFavoriteData,
    GetUserFavoriteResult,
    GetUserFavoriteCountResult,
    GetUserFavoriteCountData,
    ChangeNamesData, 
    ChangeUserBioData, 
    GetMeData, 
    GetMeResult, 
    GetUserInfoData, 
    GetUserInfoResult, 
    SetUserFavoriteData,
)

__version__ = '0.0.13'

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
            
            self.is_logged_in = True
            
        except:
            self.is_initialized = False
            raise

    async def restart(self) -> None:
        if self.is_initialized:
            self.is_initialized = False
        
        if self.is_logged_in:
            self.is_logged_in = False
        
        if self.__woto_socket:
            await self.__woto_socket.close()
        
        await self.start()
        
        
    
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
    
    async def change_user_bio(self, bio: str, user_id: int = 0) -> bool:
        response = await self.send_and_parse(
            ChangeUserBioData(
                user_id=user_id,
                bio=bio,
            ),
        )

        if not response.success:
            raise response.get_exception()
        
        return response.result

    async def change_names(self, first_name: str, last_name: str, user_id: int = 0) -> bool:
        if not first_name and not last_name:
            return False
        
        response = await self.send_and_parse(
            ChangeNamesData(
                user_id=user_id,
                first_name=first_name,
                last_name=last_name,
            ),
        )

        if not response.success:
            raise response.get_exception()
        
        return response.result

    async def get_user_info(self, user_id: Union[int, str]) -> GetUserInfoResult:
        if isinstance(user_id, str):
            try:
                user_id = int(user_id)
            except ValueError: pass
        
        data: GetUserInfoData = None
        if isinstance(user_id, int):
            data = GetUserInfoData(user_id=user_id)
        elif isinstance(user_id, str):
            data = GetUserInfoData(username=user_id)
        else:
            raise InvalidTypeException(int, type(user_id))
        
        response = await self.send_and_parse(data)

        if not response.success:
            raise response.get_exception()
        
        return response.result

    async def get_user_favorite(self, key: str, user_id: int = 0) -> GetUserFavoriteResult:
        response = await self.send_and_parse(
            GetUserFavoriteData(
                user_id=user_id,
                key=key,
            ),
        )

        if not response.success:
            raise response.get_exception()
        
        return response.result
    
    async def get_user_favorite_value(self, key: str, user_id: int = 0) -> str:
        fav = self.get_user_favorite(key, user_id)
        if isinstance(fav, GetUserFavoriteResult):
            return fav.favorite_value
        
        raise InvalidTypeException(GetUserFavoriteResult, type(fav))

    async def get_user_favorites_count(self, user_id: int = 0) -> int:
        response = await self.send_and_parse(
            GetUserFavoriteCountData(
                user_id=user_id,
            ),
        )

        if not response.success:
            raise response.get_exception()
        
        if isinstance(response.result, GetUserFavoriteCountResult):
            return response.result.favorites_count
        
        return 0

    async def set_user_favorite(self, key: str, value: str, user_id: int = 0) -> bool:
        response = await self.send_and_parse(
            SetUserFavoriteData(
                user_id=user_id,
                favorite_key=key,
                favorite_value=value,
            ),
        )

        if not response.success:
            raise response.get_exception()
        
        return response.result





