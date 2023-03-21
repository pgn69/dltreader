from typing import BinaryIO

from dlt.constants import PayloadArgumentFlag
from dlt.payloadargument import DltPayloadArgument
from dlt.header import DltHeader
from dlt.constants import DltPayloadType
from dlt.types import DltPayloadArgumentBoolType, DltPayloadArgumentSIntType, \
    DltPayloadArgumentUIntType, DltPayloadArgumentFloaType, \
    DltPayloadArgumentArayType, DltPayloadArgumentStrgType, \
    DltPayloadArgumentRawdType, DltPayloadArgumentTraiType, \
    DltPayloadArgumentStruType
from .payload import DltPayload


# mapping of payload argument types to corresponding class
PAYLOAD_ARGUMENT_CLS_MAPPING = {
    PayloadArgumentFlag.BOOL: DltPayloadArgumentBoolType,
    PayloadArgumentFlag.SINT: DltPayloadArgumentSIntType,
    PayloadArgumentFlag.UINT: DltPayloadArgumentUIntType,
    PayloadArgumentFlag.FLOA: DltPayloadArgumentFloaType,
    PayloadArgumentFlag.ARAY: DltPayloadArgumentArayType,
    PayloadArgumentFlag.STRG: DltPayloadArgumentStrgType,
    PayloadArgumentFlag.RAWD: DltPayloadArgumentRawdType,
    PayloadArgumentFlag.TRAI: DltPayloadArgumentTraiType,
    PayloadArgumentFlag.STRU: DltPayloadArgumentStruType
}


class DltPayloadVerbose(DltPayload):
    """
    verbose payload class
    """
    def type(self) -> DltPayloadType:
        """
        payload type

        :return: payload type
        :rtype: DltPayloadType
        """
        return DltPayloadType.VERBOSE

    @classmethod
    def create_from(cls, f: BinaryIO, header: DltHeader):
        obj = cls()

        # set msbf
        obj.msbf = header.standard.has_msbf()

        # set number of arguments
        obj.noar = header.extended.noar

        # parse arguments
        obj.args = []

        for _ in range(obj.noar):
            # get payload argument
            arg = DltPayloadArgument.create_from(f, obj.msbf)

            # get corresponding argument type class
            arg_type = PAYLOAD_ARGUMENT_CLS_MAPPING[arg.type]

            # create instance of the type class
            obj.args.append(
                arg_type.create_from(f, arg, obj.msbf)
            )

        return obj

    def __repr__(self) -> str:
        """
        string representation of verbose payload

        :return: string representation of verbose payload
        :rtype: str
        """
        return (
            "<DltPayloadVerbose(args=[{}])>".format(
                ",".join([
                    f"{arg.__class__.__name__}(value={arg.value})"
                    for arg in self.args
                ])
            )
        )

    def __str__(self) -> str:
        """
        string representation of the verbose payload value

        :return: verbose payload values, comma separated
        :rtype: str
        """
        return ", ".join([str(x.value) for x in self.args])
