
from .general import (
    ErrorCode,
    EndpointError,
    ClientException,
    ServerException,
    GeneralException, 
)

from .serverErrors import (
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
    EndpointError,
    ClientException,
    ServerException,
    GeneralException,
    parse_server_error,
]

