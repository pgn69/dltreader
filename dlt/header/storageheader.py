import datetime
from typing import BinaryIO

from dlt.constants import DLT_STORAGE_HEADER_PATTERN
from dlt.exceptions import DltStorageHeaderException
from dlt.typereader import TypeReader


class DltStorageHeader(TypeReader):
    """
    first header of a DLT file that starts with
    the predefined DLT pattern
    """
    @staticmethod
    def size() -> int:
        """
        DLT storage header size that is fixed to 16

        :return: size of the DLT storage header
        :rtype: int
        """
        return 16

    @property
    def datetime(self) -> datetime.datetime:
        """
        returns the unix timestamp as datetime object

        :return: datetime of unix timestamp
        :rtype: datetime.datetime
        """
        return datetime.datetime.fromtimestamp(self.unixstamp)

    @classmethod
    def create_from(
        cls: "DltStorageHeader",
        f: BinaryIO,
        msbf: bool
    ) -> "DltStorageHeader":
        """
        create DLT storage header from given file with given encoding

        :param cls: DLT storage class
        :type cls: DltStorageHeader
        :param f: file that is read
        :type f: BinaryIO
        :param msbf: if True, big endian is used
        :type msbf: bool
        :return: parsed DLT storage header
        :rtype: DltStorageHeader
        """
        # create object instance of DLT storage header
        obj = cls(msbf=msbf)

        # DLT marker
        obj.pattern = obj.read_string(f, 4)
        if obj.pattern is None:
            # pattern not set
            raise DltStorageHeaderException("pattern not set")

        elif obj.pattern != DLT_STORAGE_HEADER_PATTERN:
            # invalid pattern
            raise DltStorageHeaderException(
                f"invalid storage header pattern: '{obj.pattern}'"
            )

        # seconds
        seconds = obj.read_uint32(f, msbf=False)

        # microseconds
        microseconds = obj.read_int32(f, msbf=False)

        # unix time
        obj.unixstamp = seconds + abs(microseconds) / 1e6

        # ecu
        obj.ecu = obj.read_string(f, 4, encoding="ascii")

        return obj

    def __repr__(self):
        """
        return string representation of the DLT storage header

        :return: string representation of the DLT storage header
        :rtype: str
        """
        return (
            f"<DltStorageHeader(pattern='{self.pattern}', "
            f"datetime={self.datetime}, unixstamp={self.unixstamp}, "
            f"ecu='{self.ecu}')"
        )
