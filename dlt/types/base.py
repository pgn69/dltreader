from abc import ABC
from typing import BinaryIO

from dlt.typereader import TypeReader
from dlt.payloadargument import DltPayloadArgument


class DltPayloadArgumentBaseType(ABC):
    """
    dlt payload argument base type from which
    all types are derived
    """
    def __init__(
        self: BinaryIO,
        payload_arg: DltPayloadArgument,
        msbf: bool
    ):
        self.tr = TypeReader(msbf)
        self.payload_arg = payload_arg
        self.msbf = msbf

    @classmethod
    def create_from(
        cls,
        f: BinaryIO,
        payload_arg: DltPayloadArgument,
        msbf: bool
    ):
        """
        override this method based on type
        """
        return cls(payload_arg, msbf)

    def _get_name(self, f: BinaryIO):
        """
        get name
        """
        name = "undefined"
        if self.payload_arg.vari is True:
            # get name and unit
            name_len = self.tr.read_uint16(f)
            name = self.tr.read_string(f, name_len).decode("ascii")

        return name

    def _get_name_and_unit(self, f: BinaryIO):
        """
        get name and unit
        """
        name = "undefined"
        unit = "undefined"
        if self.payload_arg.vari:
            # get name and unit
            name_len = self.tr.read_uint16(f)
            unit_len = self.tr.read_uint16(f)
            name = self.tr.read_string(f, name_len).decode("ascii")
            unit = self.tr.read_string(f, unit_len).decode("ascii")

        return name, unit

    def __repr__(self):
        return f"<{self.__class__.__name__}({self.__dict__})>"
