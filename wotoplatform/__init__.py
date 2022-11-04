#  WotoPlatform-Py - A Python library for interacting with WotoPlatform API.
#  Copyright (C) 2021-2022  ALiwoto - <woto@kaizoku.cyou> <https://github.com/ALiwoto>
#
#  This file is part of WotoPlatform-Py.
#  
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# 
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import asyncio
import json
import inspect
import logging
from typing import Callable, Union
import uuid

from wotoplatform.types.woto_crypto.password_container import PasswordContainer256
from .utils import (
    WotoSocket,
)
from .tools import (
    DataReceiver,
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
    RawResponse,
    RawDScaffold,
    ScaffoldHolder,
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
    DeleteUserFavoriteData,
    ResolveUsernameData,
)

__version__ = '0.0.20'
log = logging.getLogger(__name__)

class WotoClient(ClientBase):
    username: str = ''
    __password: str = ''
    endpoint_url: str = ''
    auth_key: str = ''
    access_hash: str = ''
    is_initialized: bool = False
    is_logged_in: bool = False
    client_version: VersionData = None
    connection_closed_handler: Callable = None
    use_tls: bool = True
    __endpoint: str = ''
    __port: int = 0
    __woto_socket: WotoSocket = None
    __MAX_DATA_BUFFER = 8
    __internal_receiver = {}
    __read_task: asyncio.Task = None
    #__internal_loop = None
    __read_data_error: Exception = None
    

    def __init__(
        self, 
        username: str, 
        password: str, 
        endpoint: str = 'wotoplatform.kaizoku.cyou', 
        port: int = 50100,
        use_tls: bool = True
    ):
        if not username:
            raise ValueError('username cannot be empty')
        if not password:
            raise ValueError('password cannot be empty')
        
        self.username = username
        self.__password = password
        self.__endpoint = endpoint
        self.__port = port

        self.__woto_socket = WotoSocket(
            host=endpoint, 
            port=port,
            use_tls=use_tls,
            ipv6=False
        )
    
    def __del__(self) -> None:
        if self.__read_task and not self.__read_task.done():
            try:
                self.__read_task.cancel()
            except Exception: pass
        
    async def start(self) -> None:
        if self.is_initialized:
            raise ClientAlreadyInitializedException()
        
        if not self.__woto_socket:
            self.__woto_socket = WotoSocket(host=self.__endpoint, port=self.__port)
        
        if self.__read_task and not self.__read_task.done():
            try:
                self.__read_task.cancel()
            except Exception: pass
        
        self.__read_task = asyncio.create_task(self.__read_data_loop())
        
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
                    password=self.__password,
                    auth_key=self.auth_key,
                    access_hash=self.access_hash,
                )
            except WrongUsername:
                await self._register(
                    username=self.username,
                    password=self.__password,
                )
            
            self.is_logged_in = True
        except:
            self.is_initialized = False
            raise
        
        # for security reasons, set the password to None here.
        self.__password = None
    
    async def stop(self) -> None:
        self.is_initialized = False
        self.is_logged_in = False
        if self.__woto_socket:
            await self.__woto_socket.close()
            self.__woto_socket = None
        
        if self.__read_task and not self.__read_task.done():
            try: self.__read_task.cancel()
            except Exception: pass
            try: await self.__read_task
            except asyncio.CancelledError: pass
        
        
    
    async def _login(self, username: str, password: str, auth_key:str, access_hash: str) -> LoginUserResult:
        """
        Login user. Don't use this method directly, instead use start method.
        """
        
        pass_container = PasswordContainer256()
        pass_container.set_as_password(password)
        response = await self.send_and_parse(
            LoginUserData(
                username=username,
                password=pass_container,
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
        pass_container = PasswordContainer256()
        pass_container.set_as_password(password)
        response = await self.send_and_parse(
            RegisterUserData(
                username=username,
                password=pass_container,
            )
        )
        
        if not isinstance(response, RegisterUserResponse):
            raise InvalidTypeException(RegisterUserResponse, type(response))

        if not response.success:
            raise response.get_exception()
        

        return response.result
    
    def get_read_data_error(self) -> Exception:
        return self.__read_data_error
    
    async def __read_data_loop(self) -> None:
        #await self.__woto_socket.connect_OLD(self.__internal_loop)
        await self.__woto_socket.connect()
        data = None
        while self.is_initialized:
            try:
                data = await self._read_data()
            except Exception as e:
                log.error(e, exc_info=True)
                self.__read_data_error = e
                data = None
                continue
            
            if not data:
                continue
            j_value = json.loads(data)
            j_uid = str(j_value['unique_id'])
            data_receiver = self.__internal_receiver.get(j_uid, None)
            if not isinstance(data_receiver, DataReceiver):
                #TODO: call handlers....
                continue
            
            data_receiver.receive_data(j_value)
            self.__internal_receiver.pop(j_uid, None)
            

    async def _write_data(self, data: bytes):
        bb = str(len(data)).zfill(self.__MAX_DATA_BUFFER)
        bb = make_sure_byte(bb, self.__MAX_DATA_BUFFER)
        await self.__woto_socket.send(bb + data)
    
    async def _read_data(self) -> bytes:
        count = await self.__woto_socket.recv(self.__MAX_DATA_BUFFER)
        if not count:
            if not self.is_initialized or not self.connection_closed_handler:
                return #TODO: logging
            self.connection_closed_handler()
            return
        count = int(count.decode('utf-8').strip())
        return await self.__woto_socket.recv(count)
    
    async def send(self, scaffold: Scaffold, timeout: float = 3):
        if not self.is_initialized:
            raise ClientNotInitializedException()
        
        if not isinstance(scaffold, Scaffold):
            raise InvalidTypeException(Scaffold, type(scaffold))

        uid = str(uuid.uuid4())
        holder = ScaffoldHolder(uid, scaffold)
        d_receiver = DataReceiver(self.__woto_socket)
        self.__internal_receiver[uid] = d_receiver
        # await self.client_lock.acquire()
        await d_receiver.first_wait()
        await self._write_data(holder.get_as_bytes())
        await d_receiver.wait_for_data(timeout)
        r_value = d_receiver.received_data
        # self.client_lock.release()
        return r_value
    
    async def send_raw_batch(self, action: int, batch_name: str, data, timeout: float = 3) -> RawResponse:
        if not isinstance(data, str):
            data = json.dumps(data)
        
        raw_scaffold = RawDScaffold(action, batch_name, data)
        return await self.send_and_parse(raw_scaffold, timeout=timeout)

    async def send_and_parse(self, scaffold: DScaffold, timeout: float = 10) -> RScaffold:
        if not isinstance(scaffold, DScaffold) and not isinstance(scaffold, RawDScaffold):
            return None
        
        response_type = scaffold.get_response_type()
        parser_method = getattr(scaffold, 'parse_response', None)
        if not response_type and not parser_method:
            return None
        
        j_value = await self.send(scaffold, timeout=timeout)
        if parser_method and inspect.ismethod(parser_method):
            return parser_method(j_value)
        
        res = response_type(**j_value)
        return res

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
                favorite_key=key,
            ),
        )

        if not response.success:
            raise response.get_exception()
        
        return response.result
    
    async def get_user_favorite_value(self, key: str, user_id: int = 0) -> str:
        fav = await self.get_user_favorite(key, user_id)
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

    async def delete_user_favorite(self, key: str, user_id: int = 0) -> bool:
        if not isinstance(user_id, int):
            raise InvalidTypeException(int, type(user_id))
        
        response = await self.send_and_parse(
            DeleteUserFavoriteData(
                user_id=user_id,
                favorite_key=key,
            ),
        )

        if not response.success:
            raise response.get_exception()
        
        return response.result
    
    async def resolve_username(self, username: str) -> GetUserInfoResult:
        if not isinstance(username, str):
            raise InvalidTypeException(str, type(username))
        

        response = await self.send_and_parse(
            ResolveUsernameData(
                username=username,
            ),
        )

        if not response.success:
            raise response.get_exception()
        
        return response.result
        




