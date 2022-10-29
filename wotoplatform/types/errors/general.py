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

from enum import Enum
from pydantic import BaseModel

class GeneralException(Exception):
    """
    General exception for the Woto platform.
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class ClientException(GeneralException):
    """
    client-side exceptions for the Woto platform.
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

class ErrorCode(Enum):
    NoError = 0
    ErrUnknown = 1
    ErrServerUnavailable = 2
    ErrInvalidUsernameFormat = 3
    ErrInvalidPasswordFormat = 4
    ErrUsernameExists = 5
    ErrWrongUsername = 6
    ErrWrongPassword = 7
    ErrInvalidAuthKeyFormat = 8
    ErrInvalidAccessHashFormat = 9
    ErrWrongAuthKey = 10
    ErrLoginAccessHashExpired = 11
    ErrInvalidFirstName = 12
    ErrInvalidLastName = 13
    ErrInvalidTitle = 14
    ErrAlreadyAuthorized = 15
    ErrNotAuthorized = 16
    ErrNotModified = 17
    ErrBioTooLong = 18
    ErrUserNotFound = 19
    ErrFirstNameTooLong = 20
    ErrLastNameTooLong = 21
    ErrInvalidUsernameAndUserId = 22
    ErrMethodNotImplemented = 23
    ErrPermissionDenied = 24
    ErrKeyNotFound = 25
    ErrInvalidTelegramId = 26
    ErrInvalidEmail = 27

class ServerException(GeneralException):
    """
    server-side exceptions for the Woto platform.
    """
    code: ErrorCode = 0
    message: str = ''
    origin: str = ''
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"woto-platform says: [{self.code.name}] {self.message} Caused by {self.origin}."

class EndpointError(BaseModel):
    code: int
    message: str
    origin: str


