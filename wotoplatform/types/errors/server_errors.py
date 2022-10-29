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

from .general import ServerException, ErrorCode


class UnknownError(ServerException):
    message: str = ''
    origin: str = ''

    def __init__(self, message: str, origin: str):
        self.code = ErrorCode.ErrUnknown
        self.message = message
        self.origin = origin
    

class ServerUnavailable(ServerException):
    message: str = ''
    origin: str = ''

    def __init__(self, message: str, origin: str):
        self.code = ErrorCode.ErrServerUnavailable
        self.message = message
        self.origin = origin


class InvalidUsernameFormat(ServerException):
    message: str = ''
    origin: str = ''

    def __init__(self, message: str, origin: str):
        self.code = ErrorCode.ErrInvalidUsernameFormat
        self.message = message
        self.origin = origin


class InvalidPasswordFormat(ServerException):
    message: str = ''
    origin: str = ''

    def __init__(self, message: str, origin: str):
        self.code = ErrorCode.ErrInvalidPasswordFormat
        self.message = message
        self.origin = origin


class UsernameExists(ServerException):
    message: str = ''
    origin: str = ''

    def __init__(self, message: str, origin: str):
        self.code = ErrorCode.ErrUsernameExists
        self.message = message
        self.origin = origin

class WrongUsername(ServerException):
    message: str = ''
    origin: str = ''

    def __init__(self, message: str, origin: str):
        self.code = ErrorCode.ErrWrongUsername
        self.message = message
        self.origin = origin

class WrongPassword(ServerException):
    message: str = ''
    origin: str = ''

    def __init__(self, message: str, origin: str):
        self.code = ErrorCode.ErrWrongPassword
        self.message = message
        self.origin = origin


class InvalidAuthKeyFormat(ServerException):
    message: str = ''
    origin: str = ''

    def __init__(self, message: str, origin: str):
        self.code = ErrorCode.ErrInvalidAuthKeyFormat
        self.message = message
        self.origin = origin


class InvalidAccessHashFormat(ServerException):
    message: str = ''
    origin: str = ''

    def __init__(self, message: str, origin: str):
        self.code = ErrorCode.ErrInvalidAccessHashFormat
        self.message = message
        self.origin = origin

class WrongAuthKey(ServerException):
    message: str = ''
    origin: str = ''

    def __init__(self, message: str, origin: str):
        self.code = ErrorCode.ErrWrongAuthKey
        self.message = message
        self.origin = origin

class LoginAccessHashExpired(ServerException):
    message: str = ''
    origin: str = ''

    def __init__(self, message: str, origin: str):
        self.code = ErrorCode.ErrLoginAccessHashExpired
        self.message = message
        self.origin = origin

class InvalidFirstName(ServerException):
    message: str = ''
    origin: str = ''

    def __init__(self, message: str, origin: str):
        self.code = ErrorCode.ErrInvalidFirstName
        self.message = message
        self.origin = origin


class InvalidLastName(ServerException):
    message: str = ''
    origin: str = ''

    def __init__(self, message: str, origin: str):
        self.code = ErrorCode.ErrInvalidLastName
        self.message = message
        self.origin = origin


class InvalidTitle(ServerException):
    message: str = ''
    origin: str = ''

    def __init__(self, message: str, origin: str):
        self.code = ErrorCode.ErrInvalidTitle
        self.message = message
        self.origin = origin


class AlreadyAuthorized(ServerException):
    message: str = ''
    origin: str = ''

    def __init__(self, message: str, origin: str):
        self.code = ErrorCode.ErrAlreadyAuthorized
        self.message = message
        self.origin = origin


class NotAuthorized(ServerException):
    message: str = ''
    origin: str = ''

    def __init__(self, message: str, origin: str):
        self.code = ErrorCode.ErrNotAuthorized
        self.message = message
        self.origin = origin

class NotModified(ServerException):
    message: str = ''
    origin: str = ''

    def __init__(self, message: str, origin: str):
        self.code = ErrorCode.ErrNotModified
        self.message = message
        self.origin = origin


class BioTooLong(ServerException):
    message: str = ''
    origin: str = ''

    def __init__(self, message: str, origin: str):
        self.code = ErrorCode.ErrBioTooLong
        self.message = message
        self.origin = origin

class UserNotFound(ServerException):
    message: str = ''
    origin: str = ''

    def __init__(self, message: str, origin: str):
        self.code = ErrorCode.ErrUserNotFound
        self.message = message
        self.origin = origin


class FirstNameTooLong(ServerException):
    message: str = ''
    origin: str = ''

    def __init__(self, message: str, origin: str):
        self.code = ErrorCode.ErrFirstNameTooLong
        self.message = message
        self.origin = origin

class LastNameTooLong(ServerException):
    message: str = ''
    origin: str = ''

    def __init__(self, message: str, origin: str):
        self.code = ErrorCode.ErrLastNameTooLong
        self.message = message
        self.origin = origin

class InvalidUsernameAndUserId(ServerException):
    message: str = ''
    origin: str = ''

    def __init__(self, message: str, origin: str):
        self.code = ErrorCode.ErrInvalidUsernameAndUserId
        self.message = message
        self.origin = origin

class MethodNotImplemented(ServerException):
    message: str = ''
    origin: str = ''

    def __init__(self, message: str, origin: str):
        self.code = ErrorCode.ErrMethodNotImplemented
        self.message = message
        self.origin = origin

class PermissionDenied(ServerException):
    message: str = ''
    origin: str = ''

    def __init__(self, message: str, origin: str):
        self.code = ErrorCode.ErrPermissionDenied
        self.message = message
        self.origin = origin

class KeyNotFound(ServerException):
    message: str = ''
    origin: str = ''

    def __init__(self, message: str, origin: str):
        self.code = ErrorCode.ErrKeyNotFound
        self.message = message
        self.origin = origin

class InvalidTelegramId(ServerException):
    message: str = ''
    origin: str = ''

    def __init__(self, message: str, origin: str):
        self.code = ErrorCode.ErrInvalidTelegramId
        self.message = message
        self.origin = origin

class InvalidEmail(ServerException):
    message: str = ''
    origin: str = ''

    def __init__(self, message: str, origin: str):
        self.code = ErrorCode.ErrInvalidEmail
        self.message = message
        self.origin = origin
