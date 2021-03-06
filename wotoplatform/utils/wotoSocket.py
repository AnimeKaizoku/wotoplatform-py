import asyncio
import ssl

class WotoSocket:
    _host: str = ''
    _port: int = 0
    __reader: asyncio.StreamReader = None
    __writer: asyncio.StreamWriter = None
    conn_lock = asyncio.Lock()
    is_initialized: bool = False
    is_closed: bool = False

    def __init__(self, host: str, port:int) -> None:
        if not host:
            raise Exception('host is required')
        
        if not port:
            raise Exception('port is required')
        
        self._host = host
        self._port = port
    
    async def connect(self, loop = None) -> None:
        ssl_ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        ssl_ctx.check_hostname = False
        ssl_ctx.set_ciphers('ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384')
    
        r, w = await self.open_connection(
            host=self._host, 
            port=self._port,
            loop=loop,
            ssl=ssl_ctx,
            ssl_handshake_timeout=900)
        
        self.__reader = r
        self.__writer = w
        self.is_initialized = True
    

    async def open_connection(self, host=None, port=None, loop=None, *,
                            limit=asyncio.streams._DEFAULT_LIMIT, **kwds):
        """A wrapper for create_connection() returning a (reader, writer) pair.

        The reader returned is a StreamReader instance; the writer is a
        StreamWriter instance.

        The arguments are all the usual arguments to create_connection()
        except protocol_factory; most common are positional host and port,
        with various optional keyword arguments following.

        Additional optional keyword arguments are loop (to set the event loop
        instance to use) and limit (to set the buffer limit passed to the
        StreamReader).

        (If you want to customize the StreamReader and/or
        StreamReaderProtocol classes, just copy the code -- there's
        really nothing special here except some convenience.)
        """
        if not loop:
            loop = asyncio.events.get_running_loop()
        reader = asyncio.StreamReader(limit=limit, loop=loop)
        protocol = asyncio.StreamReaderProtocol(reader, loop=loop)
        transport, _ = await loop.create_connection(
            lambda: protocol, host, port, **kwds)
        writer = asyncio.StreamWriter(transport, protocol, reader, loop)
        return reader, writer




    async def send(self, data: bytes) -> None:
        while not self.__writer and not self.is_initialized:
            await asyncio.sleep(0.1)
        # await self.conn_lock.acquire()
        self.__writer.write(data)
        await self.__writer.drain()
        # self.conn_lock.release()
    
    async def recv(self, size: int) -> bytes:
        try:
            return await self.__reader.read(size)
        except IndexError:
            return b''
    
    async def close(self) -> None:
        try:
            await self.__writer.close()
            self.__reader = None
            self.__writer = None
            self.is_closed = True
        except Exception: pass
        
    