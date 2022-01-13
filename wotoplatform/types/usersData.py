
from .scaffold import (
    DScaffold,
)

__BATCH_REGISTER_USER__ = 'register_user'
__BATCH_LOGIN_USER__ = 'login_user'
__ACTION_USER__ = 1

class RegisterUserData(DScaffold):
    user_name: str = ''
    password: str = ''

    def get_action(self) -> int:
        return __ACTION_USER__
    
    def get_single_batch(self) -> str:
        return __BATCH_REGISTER_USER__

class LoginUserData(DScaffold):
    user_name: str = ''
    password: str = ''
    auth_key: str = ''
    access_hash: str = ''

    def get_action(self) -> int:
        return __ACTION_USER__
    
    def get_single_batch(self) -> str:
        return __BATCH_REGISTER_USER__



