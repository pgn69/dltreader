import logging
import socket
import asyncio
import time
from typing import Union, BinaryIO
from contextlib import ContextDecorator

from .exceptions import DltStorageHeaderException
from .header.storageheader import DltStorageHeader
from .packet import DltPacket


# prepare logger
log = logging.getLogger(__name__)


class SocketIO(BinaryIO):
    def __init__(self, socket) -> None:
        super().__init__()
        self._socket = socket

    def read(self, n):
        ret = bytearray()
        nn = 0
        while nn < n:
            r = self._socket.recv(n - nn)
            nn += len(r)
            ret.extend(r)
        return ret

    def close(self):
        self._socket.close()


class DltAsyncReceiver(ContextDecorator):
    """
    main DLT receiver class for asyncio
    """
    def __init__(self,
        host: str,
        port: int,
        msbf: bool = False
    ):
        self._host = host
        self._port = port
        self._socket = None
        self._reader = None
        self._writer = None
        self._io = None
        # if True, big endian is used
        self.msbf = msbf

    @property
    def host(self) -> str:
        return self._host

    @property
    def port(self) -> str:
        return self._port

    async def __aenter__(self) -> "DltAsyncReceiver":
        """
        enter the context

        :return: DLT receiver
        :rtype: DltReceiver
        """
        log.debug("entering DLT context...")
        await self.open()
        return self

    async def __aexit__(self, *exc):
        """
        exit the context
        """
        log.debug("leaving DLT context...")
        await asyncio.to_thread(self.close)

    def _open(self):
        """
        open the TCP connection
        """
        log.debug(f"opening DLT TCP stream {self.host}:{self.port}...")
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                self._socket.connect((self._host, self._port))
                self._io = SocketIO(self._socket)
                log.debug(f"opened DLT TCP stream {self.host}:{self.port}")
                return
            except ConnectionRefusedError:
                time.sleep(0.5)

    async def open(self):
        await asyncio.to_thread(self._open)

    def close(self):
        """
        close the TCP connection
        """
        log.debug(f"closing TCP connection {self.host}:{self.port}...")
        if self._io is not None:
            self._io.close()
            self._io = None

    def __aiter__(self) -> "DltAsyncReceiver":
        return self

    def _get_next(self):
        return None, DltPacket.create_from(
                    f=self._io,
                    msbf=self.msbf
                )

    async def __anext__(self) -> tuple:
        """
        read stream one packet after the other

        :return: tuple of DltHeader and parsed package
        :rtype: tuple
        """
        log.debug(f"reading DLT stream {self.host}:{self.port} IO {self._io} ...")
        while True:
            try:
                # read the packet and return it
                return await asyncio.to_thread(self._get_next)

            except EOFError:
                # Struct raised EOF
                log.debug(f"DLT stream {self.host}:{self.port} EOF")
                raise StopIteration()

            except Exception as e:
                # skip invalid block
                log.debug(f"{type(e)}: {e}")
