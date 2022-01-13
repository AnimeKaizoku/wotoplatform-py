
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


class ServerException(GeneralException):
    """
    server-side exceptions for the Woto platform.
    """
    code: int = 0
    message: str = ''
    origin: str = ''
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

class EndpointError(BaseModel):
    code: int
    message: str
    origin: str


