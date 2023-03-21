from typing import BinaryIO

from dlt.payloadargument import DltPayloadArgument
from .base import DltPayloadArgumentBaseType


class DltPayloadArgumentStruType(DltPayloadArgumentBaseType):
    """
    structure type
    """
    @classmethod
    def create_from(
        cls,
        f: BinaryIO,
        payload_arg: DltPayloadArgument,
        msbf: bool
    ):
        raise Exception("NOT YET IMPLEMENTED")

        # 4 - Type InfoEssential information for interpreting the Data Payload
        # x - Data PayloadData and optional additional parameters

        obj = cls(info, msbf)

        # get length
        data_len = obj.tr.read_uint16(f, msbf=obj.msbf)

        # get name and unit
        obj.name = obj._get_name(f)

        # get raw data
        obj.value = f.read(data_len)

        return obj
