import asyncio

class WotoSocket:
    _host: str = ''
    _port: int = 0
    __reader: asyncio.StreamReader = None
    __writer: asyncio.StreamWriter = None
    is_initialized: bool = False

    def __init__(self, host: str, port:int) -> None:
        if not host:
            raise Exception('host is required')
        
        if not port:
            raise Exception('port is required')
        
        self._host = host
        self._port = port
    
    async def connect(self) -> None:
        r, w = await asyncio.open_connection(host=self._host, port=self._port)
        self.__reader = r
        self.__writer = w
        self.is_initialized = True
    
    async def send(self, data: bytes) -> None:
        self.__writer.write(data)
        await self.__writer.drain()
    
    async def recv(self, size: int) -> bytes:
        return await self.__reader.read(size)
    
    async def close(self) -> None:
        try:
            await self.__writer.close()
            self.__reader = None
            self.__writer = None
        except Exception: pass
        
    