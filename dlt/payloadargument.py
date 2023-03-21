from typing import BinaryIO

from .constants import PayloadArgumentFlag, PayloadArgumentMask
from .typereader import TypeReader


class DltPayloadArgument(TypeReader):
    """
    DLT payload argument
    """
    @classmethod
    def create_from(
        cls: "DltPayloadArgument",
        f: BinaryIO,
        msbf: bool
    ) -> "DltPayloadArgument":
        """
        create DLT payload argument instance from file

        :param cls: DLT payload argument class
        :type cls: DltPayloadArgument
        :param f: binary file that is read
        :type f: BinaryIO
        :param msbf: if True, big endian is used
        :type msbf: bool
        :return: DLT payload argument instance
        :rtype: DltPayloadArgument
        """
        # create DLT payload argument instance
        obj = cls(msbf=msbf)

        # argument value on which bit-masks are applied
        obj.value = obj.read_uint32(f)

        # try to identify the type based on bits set in value
        obj.type = None
        for t in [
            PayloadArgumentFlag.BOOL, PayloadArgumentFlag.SINT,
            PayloadArgumentFlag.UINT, PayloadArgumentFlag.FLOA,
            PayloadArgumentFlag.ARAY, PayloadArgumentFlag.STRG,
            PayloadArgumentFlag.RAWD, PayloadArgumentFlag.TRAI,
            PayloadArgumentFlag.STRU
        ]:
            if (obj.value & t.value) != 0:
                # identified the type
                obj.type = t
                break

        # type length
        obj.tyle = obj.value & PayloadArgumentFlag.TYLE.value

        # variable info
        obj.vari = obj.value & PayloadArgumentFlag.VARI.value

        # bit fixed points
        obj.fixp = bool(obj.value & PayloadArgumentFlag.FIXP.value)

        # bit string coding
        obj.scod = bool(obj.value & PayloadArgumentFlag.SCOD.value)

        # get tyle value
        obj.tyle_value = (obj.value & PayloadArgumentMask.TYLE.value)

        # get scod value
        obj.scod_value = (
            (obj.value & PayloadArgumentMask.SCOD.value)
            if obj.scod
            else None
        )

        return obj

    def __repr__(self) -> str:
        return (
            f"<DltPayloadArgument(value={self.value}, type={self.type}, "
            f"tyle={self.tyle}, vari={self.vari}, fixp={self.fixp}, "
            f"scod={self.scod})>"
        )
