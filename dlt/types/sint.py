from typing import BinaryIO

from dlt.constants import TyleType
from dlt.payloadargument import DltPayloadArgument
from .base import DltPayloadArgumentBaseType


class DltPayloadArgumentSIntType(DltPayloadArgumentBaseType):
    """
    signed integer type
    """
    @classmethod
    def create_from(
        cls,
        f: BinaryIO,
        payload_arg: DltPayloadArgument,
        msbf: bool
    ):
        obj = cls(payload_arg, msbf)

        # get name and unit
        obj.name, obj.unit = obj._get_name_and_unit(f)

        # read point
        obj.point = obj._get_point(f)

        # get value
        obj.value = obj.tr.read_int(f, bits=2 ** (2 + payload_arg.tyle_value))

        return obj

    def _get_point(self, f: BinaryIO):
        """
        get point
        """
        if self.payload_arg.fixp is False:
            return "undefined"

        quantization = self.tr.read_float32(f)

        # get value based on tyle type
        offset = {
            TyleType.BIT8.value: self.tr.read_uint32,
            TyleType.BIT16.value: self.tr.read_uint32,
            TyleType.BIT32.value: self.tr.read_uint32,
            TyleType.BIT64.value: self.tr.read_uint64,
            # TyleType.BIT128.value: None,  # not supported
        }[self.payload_arg.tyle_value](f)

        return quantization, offset
