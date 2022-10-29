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

import asyncio
from .types.errors import (
    EmptyServerResponse,
    DataReceiveTimeout,
)


def make_sure_byte(b: bytes, length: int) -> bytes:
    """
    make_sure_byte is a useful function. consider b is a number in string
    and you are sending it as a byte to this function.
    this function then, will ensure that the length of this byte array
    is exactly equal to the passed-by argument.
    for example:
    make_sure_byte([]byte("5"), 8) will return []byte("5       ")
    the returned value's length will be exactly the same as length.
    """
    tmp_b = b
    while len(b) < length: tmp_b = tmp_b + b' '
    return bytes(tmp_b, 'utf-8')

class DataReceiver:
    received_data = None
    base_client = None
    _data_waiter: asyncio.Lock = None
    
    def __init__(self, base_client) -> None:
        self._data_waiter = asyncio.Lock()
        self.base_client = base_client
    
    async def wait_for_data(self, timeout: float = 20) -> bytes:
        try:
            await asyncio.wait_for(self._wait_for_data(), timeout=timeout)
        except asyncio.TimeoutError as e:
            raise DataReceiveTimeout(e)
        
        # await self._wait_for_data()
        
        if self.received_data == None:
            raise EmptyServerResponse()
        
        return self.received_data
    
    async def first_wait(self) -> None:
        if self._data_waiter.locked(): return
        await self._data_waiter.acquire()
        
    async def _wait_for_data(self) -> None:
        # while not self.received_data and not getattr(self.base_client, 'is_closed', False):
            # await asyncio.sleep(0.1)
        await self._data_waiter.acquire()
    
    def receive_data(self, data) -> None:
        self.received_data = data
        self._data_waiter.release()
    
    
    