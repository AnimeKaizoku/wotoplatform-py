
from .general import ServerException, ErrorCode

#	ErrUnknown  => 1
#	ErrServerUnavailable => 2
#	ErrInvalidUsernameFormat    => 3
#	ErrInvalidPasswordFormat    => 4
#	ErrUsernameExists        => 5
#	ErrWrongUsername    => 6
#	ErrWrongPassword    => 7
#	ErrInvalidAuthKeyFormat   => 8
#	ErrInvalidAccessHashFormat  => 9
#	ErrWrongAuthKey   => 10
#	ErrLoginAccessHashExpired    => 11
#	ErrInvalidFirstName    => 12
#	ErrInvalidLastName   => 13


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


