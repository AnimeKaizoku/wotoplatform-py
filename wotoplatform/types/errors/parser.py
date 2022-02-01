
from .general import (
    ErrorCode,
    EndpointError,
    ServerException,
)

from .serverErrors import *

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

