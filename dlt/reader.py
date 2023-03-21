import logging
from typing import Union
from pathlib import Path
from contextlib import ContextDecorator

from .exceptions import DltStorageHeaderException
from .header.storageheader import DltStorageHeader
from .packet import DltPacket


# prepare logger
log = logging.getLogger(__name__)


class DltReader(ContextDecorator):
    """
    main DLT reader class that provides context manager
    """
    def __init__(self,
        filename: Union[str, Path],
        msbf: bool = False
    ):
        self.filename = filename

        # if True, big endian is used
        self.msbf = msbf

    @property
    def filename(self) -> Path:
        """
        return DLT filename

        :return: DLT filename
        :rtype: Path
        """
        return self._filename

    @filename.setter
    def filename(
        self,
        value: Union[str, Path]
    ):
        """
        set DLT filename

        :param value: filename
        :type value: Union[str, Path]
        """
        assert isinstance(value, (str, Path))

        # ensure filename is Path
        self._filename = (
            value
            if isinstance(value, Path) else
            Path(value)
        )

    def __enter__(self) -> "DltReader":
        """
        enter the context

        :return: DLT reader
        :rtype: DltReader
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
        open the file in binary mode
        """
        log.debug(f"opening DLT file '{self.filename.as_posix()}'...")
        self._f = self.filename.open( "rb")

    def close(self):
        """
        close the file
        """
        log.debug(f"closing DLT file '{self.filename.as_posix()}'...")
        self._f.close()

    def __iter__(self) -> "DltReader":
        return self

    def __next__(self) -> tuple:
        """
        read file one packet after the other

        :return: tuple of DltStorageHeader and parsed package
        :rtype: tuple
        """
        # get storage header
        log.debug(f"reading DLT file '{self.filename.as_posix()}'...")
        while True:
            try:
                try:
                    # read storage header to ensure valid DLT block
                    dh = DltStorageHeader.create_from(
                        f=self._f,
                        msbf=self.msbf
                    )

                    # read the packet and return it
                    return dh, DltPacket.create_from(
                        f=self._f,
                        msbf=self.msbf
                    )

                except DltStorageHeaderException as e:
                    # skip invalid block with
                    # broken storage header
                    log.error(e)

            except EOFError:
                # Struct raised EOF
                raise StopIteration()
