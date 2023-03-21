from typing import BinaryIO

from dlt.payloadargument import DltPayloadArgument
from .base import DltPayloadArgumentBaseType


class DltPayloadArgumentBoolType(DltPayloadArgumentBaseType):
    """
    bool type
    """
    @classmethod
    def create_from(
        cls,
        f: BinaryIO,
        payload_arg: DltPayloadArgument,
        msbf: bool
    ):
        obj = cls(payload_arg, msbf)

        # get name
        obj.name = obj._get_name(f)

        # get bool value
        obj.value = obj.tr.read_bool(f)

        return obj
