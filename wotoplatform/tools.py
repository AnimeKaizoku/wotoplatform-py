
import asyncio
from .types.errors import (
    DataReceiveTimeout,
    EmptyServerResponse,
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
    
    def __init__(self, base_client) -> None:
        self.base_client = base_client
    
    async def wait_for_data(self, timeout: float = 60) -> bytes:
        # x = await asyncio.gather(self._wait_for_data())
        # try:
            # await asyncio.wait_for(x, timeout=timeout)
        # except asyncio.TimeoutError as e:
            # raise DataReceiveTimeout(e)
        
        await self._wait_for_data()
        
        if self.received_data == None:
            raise EmptyServerResponse()
        
        return self.received_data
    
    async def _wait_for_data(self) -> None:
        while not self.received_data and not getattr(self.base_client, 'is_closed', False):
            await asyncio.sleep(0.1)
    
    def receive_data(self, data) -> None:
        self.received_data = data
        # self._data_waiter.release()
    
    
    