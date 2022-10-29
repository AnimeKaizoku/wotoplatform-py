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

import json
import typing
from pydantic import BaseModel

from wotoplatform.types.errors.general import EndpointError
from ..errors import ServerException
from ..errors import parse_server_error

__BATCH_STR__ = 'batch?='

class Scaffold():
    def get_action(self) -> int:
        pass
    
    def get_single_batch(self) -> str:
        pass

    def get_batch_execution(self) -> str:
        return __BATCH_STR__ + self.get_single_batch()
    
    def is_empty_scaffold(self):
        return False


class ScaffoldHolder():
    """
    ScaffoldHolder is a simple scaffold container which has unique-id.
    """
    _data_unique_id: str = ''
    scaffold_data: Scaffold = None
    def get_unique_id(self) -> str:
        return self._data_unique_id
    
    def set_unique_id(self, uid: str):
        self._data_unique_id = uid
    
    def __init__(self, unique_id: str, the_data: Scaffold) -> None:
        self._data_unique_id = unique_id
        self.scaffold_data = the_data
    
    def get_as_bytes(self) -> bytes:
        final_value = {
            'unique_id': self.get_unique_id(),
            'action': self.scaffold_data.get_action(),
            'batch_execute': self.scaffold_data.get_batch_execution(),
            'data': self.scaffold_data.json(),
        }
        return json.dumps(final_value).encode('utf-8')

class DScaffold(Scaffold, BaseModel):
    """
    DScaffold is a base class for all data classes that need to be sent to the server.
    """
    pass
    
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
    RScaffold is a base class for all data classes that need to be received 
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



class RawResponse(RScaffold):
    """
    A raw server response.
    """
    result: typing.Optional[typing.Union[dict, list]]


class RawDScaffold(Scaffold):
    """
    RawDScaffold is a Scaffold which contains raw data in itself, instead of having
    attributes like normal Scaffold classes.
    """
    __scaffold_action: int = 0
    __scaffold_single_batch: str = ''
    __scaffold_json_data: str = ''
    
    def __init__(self, action: int, the_batch: str, data: str) -> None:
        self.__scaffold_action = action
        self.__scaffold_single_batch = the_batch
        self.__scaffold_json_data = data
    
    def get_action(self) -> int:
        return self.__scaffold_action
    
    def get_single_batch(self) -> str:
        return self.__scaffold_single_batch
    
    def json(self) -> str:
        return self.__scaffold_json_data
    
    def parse_response(self, j_value):
        if j_value is dict:
            my_result = j_value['result']
            j_value['result'] = None
            raw_resp = RawResponse(**j_value)
            raw_resp.result = my_result
            return raw_resp
        return RawResponse(**j_value)

    def get_response_type(self) -> type:
        return RawResponse

