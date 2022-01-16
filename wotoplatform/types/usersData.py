import typing
from .scaffold import (
    DScaffold,
    RScaffold,
    ResultScaffold,
)

__BATCH_REGISTER_USER__ = 'register_user'
__BATCH_LOGIN_USER__ = 'login_user'
__BATCH_GET_ME__ = 'get_me'
__BATCH_GET_USER_INFO__ = 'get_user_info'
__BATCH_RESOLVE_USERNAME__ = 'resolve_username'
__ACTION_USER__ = 2

class RegisterUserData(DScaffold):
    username: str = ''
    password: str = ''
    first_name: str = ''
    last_name: str = ''

    def get_action(self) -> int:
        return __ACTION_USER__
    
    def get_single_batch(self) -> str:
        return __BATCH_REGISTER_USER__
    
    def get_response_type(self) -> type:
        return RegisterUserResponse
    
class RegisterUserResult(ResultScaffold):
    is_acceptable: bool = False
    server_time: str = ''
    
class RegisterUserResponse(RScaffold):
    result: typing.Optional[RegisterUserResult]


class LoginUserData(DScaffold):
    username: str = ''
    password: str = ''
    auth_key: str = ''
    access_hash: str = ''

    def get_action(self) -> int:
        return __ACTION_USER__
    
    def get_single_batch(self) -> str:
        return __BATCH_LOGIN_USER__
    
    def get_response_type(self) -> type:
        return LoginUserResponse

class LoginUserResult(ResultScaffold):
    is_acceptable: bool = False
    server_time: str = ''
    
class LoginUserResponse(RScaffold):
    result: typing.Optional[LoginUserResult]


class GetMeData(DScaffold):
    username: str = ''
    password: str = ''
    auth_key: str = ''
    access_hash: str = ''

    def get_action(self) -> int:
        return __ACTION_USER__
    
    def get_single_batch(self) -> str:
        return __BATCH_LOGIN_USER__
    
    def get_response_type(self) -> type:
        return GetMeResponse

class GetMeResult(ResultScaffold):
    is_acceptable: bool = False
    server_time: str = ''
    
class GetMeResponse(RScaffold):
    result: typing.Optional[LoginUserResult]


class GetUserInfoData(DScaffold):
    username: str = ''
    password: str = ''
    auth_key: str = ''
    access_hash: str = ''

    def get_action(self) -> int:
        return __ACTION_USER__
    
    def get_single_batch(self) -> str:
        return __BATCH_LOGIN_USER__
    
    def get_response_type(self) -> type:
        return GetUserInfoResponse

class GetUserInfoResult(ResultScaffold):
    is_acceptable: bool = False
    server_time: str = ''
    
class GetUserInfoResponse(RScaffold):
    result: typing.Optional[LoginUserResult]


class ResolveUsernameData(DScaffold):
    username: str = ''
    password: str = ''
    auth_key: str = ''
    access_hash: str = ''

    def get_action(self) -> int:
        return __ACTION_USER__
    
    def get_single_batch(self) -> str:
        return __BATCH_LOGIN_USER__
    
    def get_response_type(self) -> type:
        return ResolveUsernameResponse

class ResolveUsernameResult(ResultScaffold):
    is_acceptable: bool = False
    server_time: str = ''
    
class ResolveUsernameResponse(RScaffold):
    result: typing.Optional[LoginUserResult]

