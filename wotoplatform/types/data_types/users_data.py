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

from typing import Optional

from wotoplatform.types.woto_crypto.password_container import PasswordContainer256

from .. import (
    DScaffold,
    RScaffold,
    ResultScaffold,
    EmptyScaffoldData,
)
from ..permissions import UserPermission



__BATCH_REGISTER_USER__             = 'register_user'
__BATCH_LOGIN_USER__                = 'login_user'
__BATCH_GET_ME__                    = 'get_me'
__BATCH_CHANGE_USER_BIO__           = 'change_user_bio'
__BATCH_CHANGE_NAMES__              = 'change_names'
__BATCH_CHANGE_USER_INFO__          = 'change_user_info'
__BATCH_GET_USER_INFO__             = 'get_user_info'
__BATCH_RESOLVE_USERNAME__          = 'resolve_username'
__BATCH_GET_USER_FAVORITE__         = 'get_user_favorite'
__BATCH_GET_USER_FAVORITE_COUNT__   = 'get_user_favorite_count'
__BATCH_SET_USER_FAVORITE__         = 'set_user_favorite'
__BATCH_DELETE_USER_FAVORITE__      = 'delete_user_favorite'


__ACTION_USER__ = 2

class RegisterUserData(DScaffold):
    user_id: int = 0
    private_hash: str = ''
    username: str = ''
    password: PasswordContainer256 = None
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
    password: PasswordContainer256 = None
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


class GetUserFavoriteData(DScaffold):
    user_id: int = 0
    favorite_key: str = ''

    def get_action(self) -> int:
        return __ACTION_USER__
    
    def get_single_batch(self) -> str:
        return __BATCH_GET_USER_FAVORITE__
    
    def get_response_type(self) -> type:
        return GetUserFavoriteResponse


class GetUserFavoriteResult(ResultScaffold):
    favorite_value: str = ''
    updated_at: str = ''

class GetUserFavoriteResponse(RScaffold):
    result: Optional[GetUserFavoriteResult]


class GetUserFavoriteCountData(DScaffold):
    user_id: int = 0

    def get_action(self) -> int:
        return __ACTION_USER__
    
    def get_single_batch(self) -> str:
        return __BATCH_GET_USER_FAVORITE_COUNT__
    
    def get_response_type(self) -> type:
        return GetUserFavoriteCountResponse


class GetUserFavoriteCountResult(ResultScaffold):
    favorites_count: int = 0

class GetUserFavoriteCountResponse(RScaffold):
    result: Optional[GetUserFavoriteCountResult]

class SetUserFavoriteData(DScaffold):
    user_id: int = 0
    favorite_key: str = ''
    favorite_value: str = ''

    def get_action(self) -> int:
        return __ACTION_USER__
    
    def get_single_batch(self) -> str:
        return __BATCH_SET_USER_FAVORITE__
    
    def get_response_type(self) -> type:
        return SetUserFavoriteResponse


class SetUserFavoriteResponse(RScaffold):
    result: Optional[bool]

class DeleteUserFavoriteData(DScaffold):
    user_id: int = 0
    favorite_key: str = ''

    def get_action(self) -> int:
        return __ACTION_USER__
    
    def get_single_batch(self) -> str:
        return __BATCH_DELETE_USER_FAVORITE__
    
    def get_response_type(self) -> type:
        return DeleteUserFavoriteResponse

class DeleteUserFavoriteResponse(RScaffold):
    result: Optional[bool]

class ResolveUsernameData(DScaffold):
    username: str = ''

    def get_action(self) -> int:
        return __ACTION_USER__
    
    def get_single_batch(self) -> str:
        return __BATCH_DELETE_USER_FAVORITE__
    
    def get_response_type(self) -> type:
        return ResolveUsernameResponse

class ResolveUsernameResponse(RScaffold):
    result: Optional[GetUserInfoResult]


class LikedItem(DScaffold):
    """
    type LikedListElement struct {
        UniqueId     string       `json:"unique_id" gorm:"primaryKey"`
        OwnerId      PublicUserId `json:"owner_id"`
        MediaId      MediaModelId `json:"media_id"`
        Title        string       `json:"title"`
        LikedKey     string       `json:"liked_key"`
        SourceUrl    string       `json:"source_url"`
        ReferenceUrl string       `json:"reference_url"`
        UpdatedAt    time.Time    `json:"-"`
    }
    """
    unique_id: str = ''
    owner_id: int = 0
    media_id: int = 0
    title: str = ''
    liked_key: str = ''
    source_url: str = ''
    reference_url: str = ''


