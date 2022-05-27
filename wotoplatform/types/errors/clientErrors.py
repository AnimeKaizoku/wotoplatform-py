
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

