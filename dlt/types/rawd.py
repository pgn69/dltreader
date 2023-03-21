from typing import BinaryIO

from dlt.payloadargument import DltPayloadArgument
from .base import DltPayloadArgumentBaseType


class DltPayloadArgumentRawdType(DltPayloadArgumentBaseType):
    """
    raw data type
    """
    @classmethod
    def create_from(
        cls,
        f: BinaryIO,
        payload_arg: DltPayloadArgument,
        msbf: bool
    ):
        obj = cls(payload_arg, msbf)

        # get length
        data_len = obj.tr.read_uint16(f)

        # get name and unit
        obj.name = obj._get_name(f)

        # get raw data
        obj.value = f.read(data_len)

        return obj
