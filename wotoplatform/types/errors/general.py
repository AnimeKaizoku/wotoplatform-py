
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


