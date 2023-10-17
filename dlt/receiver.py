import logging
import socket
from typing import Union, BinaryIO
from pathlib import Path
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


class DltReceiver(ContextDecorator):
    """
    main DLT reader class that provides context manager
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

        # if True, big endian is used
        self.msbf = msbf

    @property
    def host(self) -> str:
        return self._host

    @property
    def port(self) -> str:
        return self._port

    def __enter__(self) -> "DltReceiver":
        """
        enter the context

        :return: DLT receiver
        :rtype: DltReceiver
        """
        log.debug("entering DLT context...")

        self.open()
        return self

    def __exit__(self, *exc):
        """
        exit the context
        """
        log.debug("leaving DLT context...")

        self.close()

        return False

    def open(self):
        """
        open the TCP connection
        """
        log.debug(f"opening DLT TCP stream {self.host}:{self.port}...")
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((self._host, self._port))
        self._io = SocketIO(self._socket)

    def close(self):
        """
        close the file
        """
        log.debug(f"closing DLT file {self.host}:{self.port}...")
        if self._io is not None:
            self._io.close()
            self._io = None

    def __iter__(self) -> "DltReceiver":
        return self

    def __next__(self) -> tuple:
        """
        read stream one packet after the other

        :return: tuple of DltHeader and parsed package
        :rtype: tuple
        """
        # get header
        log.debug(f"reading DLT stream {self.host}:{self.port}...")
        while True:
            try:
                # read the packet and return it
                return None, DltPacket.create_from(
                    f=self._io,
                    msbf=self.msbf
                )

            except EOFError:
                # Struct raised EOF
                raise StopIteration()

            except Exception as e:
                # skip invalid block
                log.debug(f"{type(e)}: {e}")
        