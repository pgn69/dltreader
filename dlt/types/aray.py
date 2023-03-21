from typing import BinaryIO

from dlt.payloadargument import DltPayloadArgument
from .base import DltPayloadArgumentBaseType


class DltPayloadArgumentArayType(DltPayloadArgumentBaseType):
    @classmethod
    def create_from(
        cls,
        f: BinaryIO,
        payload_arg: DltPayloadArgument,
        msbf: bool
    ):
        raise Exception("NOT YET IMPLEMENTED")

        # Data Payload shall consist of an n-dimensional array of
        # one or more data types of bool (BOOL), signed integer (SINT),
        # unsigned integer (UINT) or float (FLOA) data types. The TYLE
        # field and FIXP field shall be interpreted as in the standard
        # data types.

        obj = cls(payload_arg, msbf)

        # get length
        data_len = obj.tr.read_uint16(f)

        # get name and unit
        obj.name = obj._get_name(f)

        # get raw data
        obj.value = f.read(data_len)

        return obj
