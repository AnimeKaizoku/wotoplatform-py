
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
