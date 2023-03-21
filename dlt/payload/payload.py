import abc
from typing import BinaryIO

from dlt.header.header import DltHeader
from dlt.constants import DltPayloadType
from dlt.exceptions import DltPayloadException


class DltPayload(abc.ABC):
    """
    payload class
    """
    @abc.abstractproperty
    def type(self) -> DltPayloadType:
        """
        override payload type by subclass

        :return: payload type
        :rtype: DltPayloadType
        """
        raise DltPayloadException("type property must be implemented!")

    @classmethod
    def create_from(
        cls: "DltPayload",
        f: BinaryIO,
        header: DltHeader
    ) -> "DltPayload":
        """
        create DLT payload from file

        :param cls: DLT payload class
        :type cls: DltPayload
        :param f: binary file that is read
        :type f: BinaryIO
        :param header: DLT header
        :type header: DltHeader
        :return: DLT payload
        :rtype: DltPayload
        """
        from .payloadnonverbose import DltPayloadNonVerbose
        from .payloadverbose import DltPayloadVerbose

        if (header.extended is None) or (header.extended.verb is False):
            # non-verbose payload, i.e., without meta information
            return DltPayloadNonVerbose.create_from(f, header)

        else:
            # verbose payload, i.e., with meta information
            return DltPayloadVerbose.create_from(f, header)

    def __repr__(self) -> str:
        """
        string representation of the DLT payload

        :return: string representation of the DLT payload
        :rtype: str
        """
        return str(self.payload)
