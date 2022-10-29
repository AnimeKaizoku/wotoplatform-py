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
    ServerException,
)

from .server_errors import *

__ERRORS_MAP__ = {
    ErrorCode.NoError: None,
    ErrorCode.ErrUnknown: UnknownError,
    ErrorCode.ErrServerUnavailable: ServerUnavailable,
    ErrorCode.ErrInvalidUsernameFormat: InvalidUsernameFormat,
    ErrorCode.ErrInvalidPasswordFormat: InvalidPasswordFormat,
    ErrorCode.ErrUsernameExists: UsernameExists,
    ErrorCode.ErrWrongUsername: WrongUsername,
    ErrorCode.ErrWrongPassword: WrongPassword,
    ErrorCode.ErrInvalidAuthKeyFormat: InvalidAuthKeyFormat,
    ErrorCode.ErrInvalidAccessHashFormat: InvalidAccessHashFormat,
    ErrorCode.ErrWrongAuthKey: WrongAuthKey,
    ErrorCode.ErrLoginAccessHashExpired: LoginAccessHashExpired,
    ErrorCode.ErrInvalidFirstName: InvalidFirstName,
    ErrorCode.ErrInvalidLastName: InvalidLastName,
    ErrorCode.ErrInvalidTitle: InvalidTitle,
    ErrorCode.ErrAlreadyAuthorized: AlreadyAuthorized,
    ErrorCode.ErrNotAuthorized: NotAuthorized,
    ErrorCode.ErrNotModified: NotModified,
    ErrorCode.ErrBioTooLong: BioTooLong,
    ErrorCode.ErrFirstNameTooLong: FirstNameTooLong,
    ErrorCode.ErrLastNameTooLong: LastNameTooLong,
    ErrorCode.ErrInvalidUsernameAndUserId: InvalidUsernameAndUserId,
    ErrorCode.ErrMethodNotImplemented: MethodNotImplemented,
    ErrorCode.ErrPermissionDenied: PermissionDenied,
    ErrorCode.ErrKeyNotFound: KeyNotFound,
    ErrorCode.ErrInvalidTelegramId: InvalidTelegramId,
    ErrorCode.ErrInvalidEmail: InvalidEmail,
}

def parse_server_error(error: EndpointError) -> ServerException:
    the_type = __ERRORS_MAP__.get(ErrorCode(error.code), None)
    if not isinstance(the_type, type):
        return UnknownError(error.message, error.origin)
    
    return the_type(error.message, error.origin)

