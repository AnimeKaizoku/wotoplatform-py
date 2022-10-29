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

from .general import (
    ErrorCode,
    EndpointError,
    ClientException,
    ServerException,
    GeneralException, 
)

from .server_errors import (
    UnknownError,
    ServerUnavailable,
    InvalidUsernameFormat,
    InvalidPasswordFormat,
    UsernameExists,
    WrongUsername,
    WrongPassword,
    InvalidAuthKeyFormat,
    InvalidAccessHashFormat,
    WrongAuthKey,
    LoginAccessHashExpired,
    InvalidFirstName,
    InvalidLastName,
    InvalidTitle,
    AlreadyAuthorized,
    BioTooLong,
    FirstNameTooLong,
    NotAuthorized,
    NotModified,
    UserNotFound,
)
from .client_errors import (
    InvalidTypeException,
    ClientVersionNotAcceptable,
    ClientNotInitializedException,
    ClientAlreadyInitializedException,
    DataReceiveTimeout,
    EmptyServerResponse
)

from .parser import (
    parse_server_error,
)


__all__ = [
    ErrorCode,
    UnknownError,
    ServerUnavailable,
    InvalidUsernameFormat,
    InvalidPasswordFormat,
    UsernameExists,
    WrongUsername,
    WrongPassword,
    InvalidAuthKeyFormat,
    InvalidAccessHashFormat,
    WrongAuthKey,
    LoginAccessHashExpired,
    InvalidFirstName,
    InvalidLastName,
    InvalidTitle,
    AlreadyAuthorized,
    BioTooLong,
    FirstNameTooLong,
    NotAuthorized,
    NotModified,
    UserNotFound,
    EndpointError,
    ClientException,
    ServerException,
    GeneralException,
    InvalidTypeException,
    ClientVersionNotAcceptable,
    ClientNotInitializedException,
    ClientAlreadyInitializedException,
    DataReceiveTimeout,
    EmptyServerResponse,
    parse_server_error,
]

