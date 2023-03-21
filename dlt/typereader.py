import struct
from typing import BinaryIO

from dlt.exceptions import TypeReaderException


class TypeReader:
    """
    helper class to read various types from DLT file
    """
    def __init__(self, msbf: bool = False):
        assert isinstance(msbf, bool)

        # if True, big endian is used
        self.msbf = msbf

    def _read(
        self,
        fmt: str,
        f: BinaryIO,
        n: int
    ) -> tuple:
        """
        helper to read n bytes from the file and unpack in the given format;
        raises eof exception at the end of file

        :param fmt: format used for unpacking
        :type fmt: str
        :param f: file object that is read
        :type f: BinaryIO
        :param n: number of bytes that is read
        :type n: int
        :raises EOFError: end of file error, if data is 0
        :return: tuple of unpacked values
        :rtype: tuple
        """
        data = f.read(n)
        if len(data) == 0:
            raise EOFError

        return struct.unpack(fmt, data)[0]

    def prefix(
        self,
        msbf: bool = None
    ) -> str:
        """
        set prefix '<' little endian or '>' big endian prefix

        :param msbf: if True, big endian is used, default is None
        :type msbf: bool, optional (if not set object's default is used)
        :return: prefix type
        :rtype: str
        """
        msbf = msbf or self.msbf

        # set
        return ">" if msbf is True else "<"

    def read_bool(
        self,
        f: BinaryIO,
        msbf: bool = None
    ) -> bool:
        """
        read 8 bit bool
        (no difference between LE and BE)

        :param f: file object that is read
        :type f: BinaryIO
        :param msbf: if True, big endian is used, default is None
        :type msbf: bool, optional (if not set object's default is used)
        :return: read bool
        :rtype: bool
        """
        return self._read(f"{self.prefix(msbf)}?", f, 1)

    def read_int8(
        self,
        f: BinaryIO,
        msbf: bool = None
    ) -> int:
        """
        read 8 bit integer
        (no difference between LE and BE)

        :param f: file object that is read
        :type f: BinaryIO
        :param msbf: if True, big endian is used, default is None
        :type msbf: bool, optional (if not set object's default is used)
        :return: read int
        :rtype: int
        """
        return self._read(f"{self.prefix(msbf)}b", f, 1)

    def read_int16(
        self,
        f: BinaryIO,
        msbf: bool = None
    ) -> int:
        """
        read 16 bit integer

        :param f: file object that is read
        :type f: BinaryIO
        :param msbf: if True, big endian is used, default is None
        :type msbf: bool, optional (if not set object's default is used)
        :return: read int
        :rtype: int
        """
        return self._read(f"{self.prefix(msbf)}h", f, 2)

    def read_int32(
        self,
        f: BinaryIO,
        msbf: bool = None
    ) -> int:
        """
        read 32 bit integer

        :param f: file object that is read
        :type f: BinaryIO
        :param msbf: if True, big endian is used, default is None
        :type msbf: bool, optional (if not set object's default is used)
        :return: read int
        :rtype: int
        """
        return self._read(f"{self.prefix(msbf)}i", f, 4)

    def read_int64(
        self,
        f: BinaryIO,
        msbf: bool = None
    ) -> int:
        """
        read 64 bit unsigned integer

        :param f: file object that is read
        :type f: BinaryIO
        :param msbf: if True, big endian is used, default is None
        :type msbf: bool, optional (if not set object's default is used)
        :return: read int
        :rtype: int
        """
        return self._read(f"{self.prefix(msbf)}q", f, 8)

    def read_int(
        self,
        f: BinaryIO,
        bits: int,
        msbf: bool = None
    ) -> int:
        """
        read int with given number of bits

        :param f: file object that is read
        :type f: BinaryIO
        :param bits: number of bits
        :type bits: int
        :param msbf: if True, big endian is used, default is None
        :type msbf: bool, optional (if not set object's default is used)
        :return: read int
        :rtype: int
        """
        func = {
            8: self.read_int8,
            16: self.read_int16,
            32: self.read_int32,
            64: self.read_int64
        }.get(bits, None)

        if func is None:
            # unknown bits
            raise TypeReaderException(f"unknown bit size '{bits}'")

        # apply function and return result
        return func(f=f, msbf=msbf)

    def read_uint8(
        self,
        f: BinaryIO,
        msbf: bool = None
    ) -> int:
        """
        read 8 bit unsigned integer
        (no difference between LE and BE)

        :param f: file object that is read
        :type f: BinaryIO
        :param msbf: if True, big endian is used, default is None
        :type msbf: bool, optional (if not set object's default is used)
        :return: read int
        :rtype: int
        """
        return self._read(f"{self.prefix(msbf)}B", f, 1)

    def read_uint16(
        self,
        f: BinaryIO,
        msbf: bool = None
    ) -> int:
        """
        read 16 bit unsigned integer

        :param f: file object that is read
        :type f: BinaryIO
        :param msbf: if True, big endian is used, default is None
        :type msbf: bool, optional (if not set object's default is used)
        :return: read int
        :rtype: int
        """
        return self._read(f"{self.prefix(msbf)}H", f, 2)

    def read_uint32(
        self,
        f: BinaryIO,
        msbf: bool = None
    ) -> int:
        """
        read 32 bit unsigned integer

        :param f: file object that is read
        :type f: BinaryIO
        :param msbf: if True, big endian is used, default is None
        :type msbf: bool, optional (if not set object's default is used)
        :return: read int
        :rtype: int
        """
        return self._read(f"{self.prefix(msbf)}I", f, 4)

    def read_uint64(
        self,
        f: BinaryIO,
        msbf: bool = None
    ) -> int:
        """
        read 64 bit unsigned integer

        :param f: file object that is read
        :type f: BinaryIO
        :param msbf: if True, big endian is used, default is None
        :type msbf: bool, optional (if not set object's default is used)
        :return: read int
        :rtype: int
        """
        return self._read(f"{self.prefix(msbf)}Q", f, 8)

    def read_uint(
        self,
        f: BinaryIO,
        bits: int,
        msbf: bool = None
    ):
        """
        read uint with given number of bits

        :param f: file object that is read
        :type f: BinaryIO
        :param bits: number of bits
        :type bits: int
        :param msbf: if True, big endian is used, default is None
        :type msbf: bool, optional (if not set object's default is used)
        :return: read int
        :rtype: int
        """
        func = {
            8: self.read_uint8,
            16: self.read_uint16,
            32: self.read_uint32,
            64: self.read_uint64
        }.get(bits, None)

        if func is None:
            # unknown bits
            raise TypeReaderException(f"unknown bit size '{bits}'")

        # apply function and return result
        return func(f=f, msbf=msbf)

    def read_float16(
        self,
        f: BinaryIO,
        msbf: bool = None
    ) -> float:
        """
        read 16 bit (half-)float

        :param f: file object that is read
        :type f: BinaryIO
        :param msbf: if True, big endian is used, default is None
        :type msbf: bool, optional (if not set object's default is used)
        :return: read float
        :rtype: float
        """
        return self._read(f"{self.prefix(msbf)}e", f, 2)

    def read_float32(
        self,
        f: BinaryIO,
        msbf: bool = None
    ) -> float:
        """
        read 32 bit float

        :param f: file object that is read
        :type f: BinaryIO
        :param msbf: if True, big endian is used, default is None
        :type msbf: bool, optional (if not set object's default is used)
        :return: read float
        :rtype: float
        """
        return self._read(f"{self.prefix(msbf)}f", f, 4)

    def read_double64(
        self,
        f: BinaryIO,
        msbf: bool = None
    ) -> float:
        """
        read 64 bit double

        :param f: file object that is read
        :type f: BinaryIO
        :param msbf: if True, big endian is used, default is None
        :type msbf: bool, optional (if not set object's default is used)
        :return: read float
        :rtype: float
        """
        return self._read(f"{self.prefix(msbf)}d", f, 8)

    def read_string(
        self,
        f: BinaryIO,
        n: int,
        encoding="ascii",
        msbf: bool = None
    ) -> str:
        """
        read string of given length

        :param f: file object that is read
        :type f: BinaryIO
        :param n: lenght of string
        :type n: int
        :param encoding: encoding
        :type encoding: str
        :param msbf: if True, big endian is used, default is None
        :type msbf: bool, optional (if not set object's default is used)
        :return: read string of given size
        :rtype: str

        """
        return self._read(
            fmt=f"{self.prefix(msbf)}{n}s", f=f, n=n
        ).decode(encoding)
