from typing import BinaryIO

from dlt.typereader import TypeReader
from dlt.constants import DltSize, DltStandardHeaderExtendedFlags, \
    DltStandardHeaderExtendedFlags, DltStandardHeaderType


class DltStandardHeader(TypeReader):
    """
    DLT standard header
    """
    @property
    def version(self) -> int:
        """
        returns the version of the protocol

        :return: version number
        :rtype: int
        """
        return (self.htyp & DltStandardHeaderExtendedFlags.VERS.value) >> 5

    def size(self) -> int:
        """
        size of the DLT standard header
        (htyp (1) + mcnt (1) + length (2) = 4 + extra size)

        :return: size of the DLT standard header
        :rtype: int
        """
        return 4 + self.header_extra_size()

    def has_ueh(self) -> bool:
        """
        returns True, if extended header is used

        :return: True, if extended header is used
        :rtype: bool
        """
        return bool(self.htyp & DltStandardHeaderType.UEH.value)

    def has_msbf(self) -> bool:
        """
        returns True if big endian else little endian

        :return: True, if big endian is used
        :rtype: bool
        """
        return bool(self.htyp & DltStandardHeaderType.MSBF.value)

    def has_weid(self) -> bool:
        """
        returns True if ECU ID is used

        :return: True, if ECI ID is used
        :rtype: bool
        """
        return bool(self.htyp & DltStandardHeaderType.WEID.value)

    def has_wsid(self) -> bool:
        """
        returns True if session id is used

        :return: True, if session ID is used
        :rtype: bool
        """
        return bool(self.htyp & DltStandardHeaderType.WSID.value)

    def has_wtms(self) -> bool:
        """
        returns True if timestamp is used

        :return: True, if timestamp is used
        :rtype: bool
        """
        return bool(self.htyp & DltStandardHeaderType.WTMS.value)

    def header_extra_size(self) -> int:
        """
        returns the extra header size that depends
        on the bits set in the header type

        :return: size of the extra header
        :rtype: int
        """
        return (
            (DltSize.WEID.value if self.has_weid() else 0) +
            (DltSize.WSID.value if self.has_wsid() else 0) +
            (DltSize.WTMS.value if self.has_wtms() else 0)
        )

    @classmethod
    def create_from(
        cls: "DltStandardHeader",
        f: BinaryIO,
        msbf: bool
    ) -> "DltStandardHeader":
        """
        create DLT standard header from given file with given encoding

        :param cls: DLT standard header class
        :type cls: DltStandardHeader
        :param f: binary file that is read
        :type f: BinaryIO
        :param msbf: if True, big endian is used
        :type msbf: bool
        :return: DLT standard header
        :rtype: DltStandardHeader
        """
        # create instance of DLT standard header
        obj = cls(msbf=msbf)

        # set header type
        obj.htyp = obj.read_uint8(f)

        # set version
        obj.vers = (
            (obj.htyp & DltStandardHeaderExtendedFlags.VERS.value) >> 5
        )

        # set message counter
        obj.mcnt = obj.read_uint8(f)

        # set length
        obj.len = obj.read_uint16(f, msbf=True)

        # set ECU ID
        obj.eid = obj.read_string(f, 4) if obj.has_weid() else ""

        # set session id
        obj.sid = obj.read_uint32(f) if obj.has_wsid() else ""

        # set timestamp
        obj.tms = obj.read_uint32(f) if obj.has_wtms() else ""

        return obj

    def __repr__(self) -> str:
        """
        return string representation of the DLT standard header

        :return: string representation of the DLT standard header
        :rtype: str
        """
        return (
            f"<DltStandardHeader(htyp={self.htyp} [UEH={self.has_ueh()}, "
            f"MSBF={self.has_msbf()}, WEID={self.has_weid()}, "
            f"WSID={self.has_wsid()}, WTMS={self.has_wtms()}], "
            f"version={self.vers}, "
            f"mcnt={self.mcnt}, len={self.len}, eid='{self.eid}', "
            f"sid='{self.sid}', tms={self.tms})"
        )
