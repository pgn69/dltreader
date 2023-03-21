from typing import BinaryIO
import logging

from .exceptions import PacketException
from .header import DltHeader
from .payload import DltPayload


# prepare logger
log = logging.getLogger(__name__)


class DltPacket:
    """
    packet
    """
    @property
    def len(self) -> int:
        """
        returns the length based on standard header

        :return: length of the packet
        :rtype: int
        """
        if (self.header is None) or (self.header.standard is None):
            raise PacketException(
                "Size of DltPacket cannot be obtained, since "
                "standard header is not set!"
            )

        return self.header.standard.len

    def has_payload(self) -> bool:
        """
        returns True, if packet has payload

        :return: True, if packet has payload
        :rtype: bool
        """
        return (
            (self.header is not None) and
            (self.header.payload_size() > 0)
        )

    @classmethod
    def create_from(
        cls: "DltPacket",
        f: BinaryIO,
        msbf: bool
    ) -> "DltPacket":
        """
        create packet instance from file

        :param cls: packet class
        :type cls: Packet
        :param f: binary file that is read
        :type f: BinaryIO
        :param msbf: if True, big endian is used
        :type msbf: bool
        :return: packet instance
        :rtype: Packet
        """
        # create packet instance
        obj = cls()

        # get header
        obj.header = DltHeader.create_from(f, msbf=msbf)
        if obj.header is None:
            # invalid packet header
            raise PacketException("Invalid packet header!")

        elif obj.header.standard is None:
            # failed to read standard header
            raise PacketException("Fail to read standard header!")

        log.debug(
            f"header_size={obj.header.header_size()}, "
            f"payload_size={obj.header.payload_size()}"
        )

        if obj.has_payload():
            # get payload (will be resolved to verbose and non-verbose payload)
            obj.payload = DltPayload.create_from(f, obj.header)

        else:
            # not payload
            obj.payload = None

        log.debug(f"payload={obj.payload}")

        return obj

    def __repr__(self) -> str:
        """
        string representation of packet

        :return: string representation of packet
        :rtype: str
        """
        return (
            f"{self.header.standard}\n{self.header.extended}\n"
            f"{self.payload}"
        )

    def __str__(self) -> str:
        """
        string representation of the packet that is
        the string presentation of the included payload

        :return: packet's payload as string
        :rtype: str
        """
        return str(self.payload)
