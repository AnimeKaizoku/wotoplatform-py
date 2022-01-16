
from .general import (
    ErrorCode,
    EndpointError,
    ServerException,
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
    AlreadyAuthorized,
    NotAuthorized,
)

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
}

def parse_server_error(error: EndpointError) -> ServerException:
    the_type = __ERRORS_MAP__.get(ErrorCode(error.code), None)
    if not isinstance(the_type, type):
        return UnknownError(error.message, error.origin)
    
    return the_type(error.message, error.origin)

