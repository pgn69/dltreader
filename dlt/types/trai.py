from typing import BinaryIO

from dlt.payloadargument import DltPayloadArgument
from .base import DltPayloadArgumentBaseType


class DltPayloadArgumentTraiType(DltPayloadArgumentBaseType):
    """
    trai type
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

        if payload_arg.scod_value == 0:
            # ascii
            obj.value = obj.tr.read_string(
                f, data_len
            ).encode("ascii")

        else:
            # utf-8
            obj.value = obj.tr.read_string(
                f, data_len
            ).encode("utf-8", "ignore")

        return obj
