from typing import Optional

from . import (
    DScaffold,
    RScaffold,
    ResultScaffold,
    EmptyScaffoldData,
)
from .permissions import UserPermission

__BATCH_REGISTER_USER__     = 'register_user'
__BATCH_LOGIN_USER__        = 'login_user'
__BATCH_GET_ME__            = 'get_me'
__BATCH_CHANGE_USER_BIO__   = 'change_user_bio'
__BATCH_CHANGE_NAMES__      = 'change_names'
__BATCH_CHANGE_USER_INFO__  = 'change_user_info'
__BATCH_GET_USER_INFO__     = 'get_user_info'
__BATCH_RESOLVE_USERNAME__  = 'resolve_username'

__ACTION_USER__ = 2

class RegisterUserData(DScaffold):
    user_id: int = 0
    private_hash: str = ''
    username: str = ''
    password: str = ''
    first_name: str = ''
    last_name: str = ''
    email: str = ''
    permission: UserPermission = UserPermission.NormalUser

    def get_action(self) -> int:
        return __ACTION_USER__
    
    def get_single_batch(self) -> str:
        return __BATCH_REGISTER_USER__
    
    def get_response_type(self) -> type:
        return RegisterUserResponse
    
class RegisterUserResult(ResultScaffold):
    user_id: int = 0
    private_hash: str = ''
    email: str = ''
    website: str = ''
    auth_key: str = ''
    access_hash: str = ''
    permission: UserPermission = UserPermission.NormalUser
    bio: str = ''
    source_url: str = ''
    telegram_id: int = 0
    first_name: str = ''
    last_name: str = ''
    username: str = ''
    created_at: str = ''
    updated_at: str = ''
    is_virtual: bool = False
    created_by: int = 0
    
class RegisterUserResponse(RScaffold):
    result: Optional[RegisterUserResult]


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
    user_id: int = 0
    private_hash: str = ''
    email: str = ''
    website: str = ''
    permission: UserPermission = UserPermission.NormalUser
    bio: str = ''
    source_url: str = ''
    telegram_id: int = 0
    first_name: str = ''
    last_name: str = ''
    username: str = ''
    created_at: str = ''
    updated_at: str = ''
    is_virtual: bool = False
    created_by: int = 0
    
class LoginUserResponse(RScaffold):
    result: Optional[LoginUserResult]


class GetMeData(EmptyScaffoldData):
    def get_action(self) -> int:
        return __ACTION_USER__
    
    def get_single_batch(self) -> str:
        return __BATCH_GET_ME__
    
    def get_response_type(self) -> type:
        return GetMeResponse

class GetMeResult(ResultScaffold):
    user_id: int = 0
    private_hash: str = ''
    email: str = ''
    website: str = ''
    permission: UserPermission = UserPermission.NormalUser
    bio: str = ''
    source_url: str = ''
    telegram_id: int = 0
    first_name: str = ''
    last_name: str = ''
    username: str = ''
    created_at: str = ''
    updated_at: str = ''
    is_virtual: bool = False
    created_by: int = 0
    
class GetMeResponse(RScaffold):
    result: Optional[LoginUserResult]


class ChangeUserBioData(DScaffold):
    user_id: int = 0
    bio: str = ''

    def get_action(self) -> int:
        return __ACTION_USER__
    
    def get_single_batch(self) -> str:
        return __BATCH_CHANGE_USER_BIO__
    
    def get_response_type(self) -> type:
        return ChangeUserBioResponse

class ChangeUserBioResponse(RScaffold):
    result: Optional[bool]


class ChangeNamesData(DScaffold):
    user_id: int = 0
    first_name: str = ''
    last_name: str = ''

    def get_action(self) -> int:
        return __ACTION_USER__
    
    def get_single_batch(self) -> str:
        return __BATCH_CHANGE_NAMES__
    
    def get_response_type(self) -> type:
        return ChangeUserBioResponse

class ChangeUserBioResponse(RScaffold):
    result: Optional[bool]


class GetUserInfoData(DScaffold):
    user_id: int = 0
    username: str = ''

    def get_action(self) -> int:
        return __ACTION_USER__
    
    def get_single_batch(self) -> str:
        return __BATCH_GET_USER_INFO__
    
    def get_response_type(self) -> type:
        return GetUserInfoResponse

class GetUserInfoResult(ResultScaffold):
    user_id: int = 0
    email: str = ''
    region: str = ''
    language: str = ''
    birthday: str = ''
    anilist_url: str = ''
    my_animelist_url: str = ''
    reddit_url: str = ''
    github_url: str = ''
    gitlab_url: str = ''
    favorite_color: str = ''
    favorite_music: str = ''
    favorite_anime: str = ''
    favorite_movie: str = ''
    favorite_food: str = ''
    favorite_series: str = ''
    favorite_light_novel: str = ''
    favorite_novel: str = ''
    website: str = ''
    permission: UserPermission = UserPermission.NormalUser
    bio: str = ''
    source_url: str = ''
    telegram_id: int = 0
    first_name: str = ''
    last_name: str = ''
    username: str = ''
    created_at: str = ''
    updated_at: str = ''
    is_virtual: bool = False
    
class GetUserInfoResponse(RScaffold):
    result: Optional[GetUserInfoResult]


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
    result: Optional[LoginUserResult]

