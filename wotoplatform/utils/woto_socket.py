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
import ssl
import sys
import socket
import time

try:
    import socks
except ImportError as e:
    e.msg = (
        "PySocks is missing and wotoplatform can't run without. "
        "Please install it using \"pip3 install pysocks\"."
    )

    raise e


class WotoSocket:
    TIMEOUT = 10
    
    _host: str = ''
    _port: int = 0
    _use_tls: bool = True
    _ipv6: bool = False
    _socket: socks.socksocket = None
    __reader: asyncio.StreamReader = None
    __writer: asyncio.StreamWriter = None
    conn_lock: asyncio.Lock = None
    is_initialized: bool = False
    is_closed: bool = False

    def __init__(
        self, 
        host: str, 
        port:int, 
        use_tls: bool, 
        ipv6: bool
    ) -> None:
        if not host:
            raise Exception('host is required')
        
        if not port:
            raise Exception('port is required')
        
        self.conn_lock = asyncio.Lock()
        self._host = host
        self._port = port
        self._use_tls = use_tls
        self._ipv6 = ipv6
        self.socket = socks.socksocket(
            socket.AF_INET6 if ipv6
            else socket.AF_INET
        )
        self.socket.settimeout(WotoSocket.TIMEOUT)
    
    async def connect(self, address: tuple = None):
        if address == None:
            address = (self._host, self._port)
        self.socket.connect(address)
        self.__reader, self.__writer = await asyncio.open_connection(sock=self.socket)
    
    async def connect_OLD(self, loop = None) -> None:
        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        ssl_ctx = None
        if self._use_tls:    
            ssl_ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            ssl_ctx.check_hostname = False
            ssl_ctx.set_ciphers('ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384')

        r, w = await self.open_connection(
            host=self._host, 
            port=self._port,
            loop=loop,
            ssl=ssl_ctx,
            ssl_handshake_timeout=9
        )
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
        
        async with self.conn_lock:
            self.__writer.write(data)
            await self.__writer.drain()
    
    async def recv(self, size: int) -> bytes:
        try:
            return await self.__reader.read(size)
        except IndexError:
            return b''
    
    async def close(self) -> None:
        try:
            try:
                self.__writer.close()
            except AttributeError:
                try:
                    self.socket.shutdown(socket.SHUT_RDWR)
                except OSError:
                    pass
                finally:
                    # A tiny sleep placed here helps avoiding .recv(n) hanging until the timeout.
                    # This is a workaround that seems to fix the occasional delayed stop of a client.
                    time.sleep(0.001)
                    self.socket.close()
            self.__reader = None
            self.__writer = None
            self.is_closed = True
        except Exception: pass
        
    