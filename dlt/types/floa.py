from typing import BinaryIO

from dlt.constants import TyleType
from dlt.payloadargument import DltPayloadArgument
from .base import DltPayloadArgumentBaseType


class DltPayloadArgumentFloaType(DltPayloadArgumentBaseType):
    """
    float type
    """
    @classmethod
    def create_from(
        cls,
        f: BinaryIO,
        payload_arg: DltPayloadArgument,
        msbf: bool
    ):
        obj = cls(payload_arg, msbf)

        # get name in unit
        obj.name, obj.unit = obj._get_name_and_unit(f)

        # get value based on tyle type
        obj.value = {
            TyleType.BIT8.value: None,    # not supported
            TyleType.BIT16.value: obj.tr.read_float16,
            TyleType.BIT32.value: obj.tr.read_float32,
            TyleType.BIT64.value: obj.tr.read_double64,
            TyleType.BIT128.value: None,  # not supported
        }[payload_arg.tyle_value](f)

        return obj
