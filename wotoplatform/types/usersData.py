import typing
from .scaffold import (
    DScaffold,
    RScaffold,
    ResultScaffold,
)

__BATCH_REGISTER_USER__ = 'register_user'
__BATCH_LOGIN_USER__ = 'login_user'
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


