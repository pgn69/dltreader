from typing import BinaryIO

from dlt.constants import ScodType
from dlt.payloadargument import DltPayloadArgument
from .base import DltPayloadArgumentBaseType


class DltPayloadArgumentStrgType(DltPayloadArgumentBaseType):
    """
    string type
    """
    @classmethod
    def create_from(
        cls,
        f: BinaryIO,
        payload_arg: DltPayloadArgument,
        msbf: bool
    ):
        obj = cls(payload_arg, msbf)

        # get length of string
        str_len = obj.tr.read_uint16(f)

        # get name
        obj.name = obj._get_name(f)

        # get encoding
        encoding = {
            ScodType.ASCII.value: "ascii",
            ScodType.UTF8.value: "utf8",
        }.get(payload_arg.scod_value or ScodType.UTF8.value)

        # read the string and do encoding
        obj.value = obj.tr.read_string(f, str_len, encoding=encoding)

        return obj
