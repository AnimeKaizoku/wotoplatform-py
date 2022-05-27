import json
import typing
from pydantic import BaseModel
from pydantic.config import Extra

from wotoplatform.types.errors.general import EndpointError
from .errors import ServerException
from .errors import parse_server_error

__BATCH_STR__ = 'batch?='

class Scaffold():
    def get_as_bytes(self) -> bytes:
        pass

    def get_action(self) -> int:
        pass

    def get_unique_id(self) -> str:
        return getattr(self, 'data_unique_id', None)
    
    def set_unique_id(self, uid: str):
        setattr(self, 'data_unique_id', uid)
    
    def get_single_batch(self) -> str:
        pass

    def get_batch_execution(self) -> str:
        return __BATCH_STR__ + self.get_single_batch()
    
    def is_empty_scaffold(self):
        return False


class DScaffold(Scaffold, BaseModel):
    """
    DScaffold is a base class for all data classes that need to be sent to the server.
    """
    def get_as_bytes(self) -> bytes:
        final_value = {
            'unique_id': self.get_unique_id(),
            'action': self.get_action(),
            'batch_execute': self.get_batch_execution(),
            'data': self.json(),
        }
        return json.dumps(final_value).encode('utf-8')
    
    def get_response_type(self) -> type:
        pass
    


class EmptyScaffoldData(DScaffold):
    """
    EmptyScaffoldData describes an empty `DScaffold`.
    """
    def is_empty_scaffold(self):
        return True
    

class ResultScaffold(BaseModel):
    """
    ResultScaffold is a base class for all data classes that need to be received
        from the server as the result itself.
    """

    def __str__(self) -> str:
        try:
            return self.json(indent=4, ensure_ascii=False)
        except Exception: return super().__str__()

class RScaffold(Scaffold, BaseModel):
    """
    RSScaffold is a base class for all data classes that need to be received 
        from the server as the response.
    """
    success: bool
    error: typing.Optional[EndpointError]
    result: typing.Optional[ResultScaffold]
    def get_action(self) -> int:
        pass

    def get_single_batch(self) -> str:
        pass

    def has_exception(self) -> bool:
        return self.error is not None
    
    def get_exception(self) -> ServerException:
        if self.has_exception():
            return parse_server_error(self.error)
        return None
