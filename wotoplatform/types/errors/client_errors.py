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
from .general import ClientException


class InvalidTypeException(ClientException):
    """
    Invalid type exception.
    """
    def __init__(self, expected_type: type, actual_type: type):
        self.expected_type = expected_type
        self.actual_type = actual_type
        self.message = f'Expected type of {expected_type}, got {actual_type}.'

class ClientNotInitializedException(ClientException):
    """
    Client not initialized exception.
    """
    def __init__(self):
        self.message = 'Client is not initialized.'

class ClientAlreadyInitializedException(ClientException):
    """
    Client already initialized exception.
    """
    def __init__(self):
        self.message = 'Client is already initialized.'

class ClientVersionNotAcceptable(ClientException):
    """
    Client version is not acceptable.
    """
    def __init__(self):
        self.message = f'Client version is not acceptable.'

class DataReceiveTimeout(ClientException):
    inner_exception: asyncio.TimeoutError = None
    """
    Client version is not acceptable.
    """
    def __init__(self, inner_exception: asyncio.TimeoutError = None):
        self.message = f'Receiving data from server timed out.'
        self.inner_exception = inner_exception

class EmptyServerResponse(ClientException):
    """
    Client version is not acceptable.
    """
    def __init__(self):
        self.message = f'Received empty data from server, most likely connection is closed.'

