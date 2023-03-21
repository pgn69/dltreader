from typing import BinaryIO
import logging

from dlt.constants import DltStandardHeaderExtendedMask, DltMessageType, \
    DltLogLevelType, DltAppTraceType, DltNetworkTraceType, DltControlType
from dlt.typereader import TypeReader


# prepare logger
log = logging.getLogger(__name__)


class DltExtendedHeader(TypeReader):
    """
    DLT extended header
    """
    def size(self) -> int:
        """
        size of the DLT extended header, fixed to 10

        :return: size of the DLT extended header
        :rtype: int
        """
        return 10

    @classmethod
    def create_from(
        cls: "DltExtendedHeader",
        f: BinaryIO,
        msbf: bool
    ) -> "DltExtendedHeader":
        """
        create DLT extended header from file

        :param cls: DLT extended header
        :type cls: DltExtendedHeader
        :param f: binary file that is read
        :type f: BinaryIO
        :param msbf: if True, big endian is used
        :type msbf: bool
        :return: DLT extended header instance
        :rtype: DltExtendedHeader
        """
        # create DLT extended header instance
        obj = cls(msbf=msbf)

        # message info
        obj.msin = obj.read_uint8(f)

        # verbose (if True, payload must be verbose)
        obj.verb = bool(
            obj.msin & DltStandardHeaderExtendedMask.VERB.value
        )

        # message type
        obj.mstp = DltMessageType(
            (obj.msin & DltStandardHeaderExtendedMask.MSTP.value) >> 1
        )

        # message info
        mtin_value = (
            (obj.msin & DltStandardHeaderExtendedMask.MTIN.value) >> 4
        )

        try:
            # depending on message type set message info
            obj.mtin = {
                DltMessageType.LOG: DltLogLevelType,
                DltMessageType.APP_TRACE: DltAppTraceType,
                DltMessageType.NW_TRACE: DltNetworkTraceType,
                DltMessageType.CONTROL: DltControlType,
            }[obj.mstp](mtin_value)

        except ValueError:
            # invalid value
            log.error(f"Invalid value '{mtin_value}' for '{obj.mstp}'!")
            obj.mtin = None

        # number of arguments
        obj.noar = obj.read_uint8(f)

        # application ID
        obj.apid = obj.read_string(f, 4)

        # context ID
        obj.ctid = obj.read_string(f, 4)

        # do self check
        obj.check()

        return obj

    def check(self):
        """
        check extended header
        """
        if (self.verb is False) and (self.noar != 0x00):
            # ensure that no arguments are provided in non-verbose mode
            log.warning(
                "in non-verbose mode the number of arguments (noar) "
                "shall be '0x00'"
            )

    def __repr__(self) -> str:
        """
        string representation of the extended DLT header

        :return: string representation of the extended DLT header
        :rtype: str
        """
        return (
            f"<DltExtendedHeader(msin={self.msin}, "
            f"verb={self.verb}, mstp={self.mstp}, mtin={self.mtin}, "
            f"noar={self.noar}, apid='{self.apid}', ctid='{self.ctid}')"
        )
