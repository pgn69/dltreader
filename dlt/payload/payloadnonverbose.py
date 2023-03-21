import logging
from typing import BinaryIO

from dlt.typereader import TypeReader
from dlt.header import DltHeader
from dlt.constants import DltPayloadType
from dlt.services import DltSetDefaultTraceStatusRequest, \
    DltGetLogInfoRequest, DltSetDefaultLogLevelRequest, \
    DltStoreConfigurationRequest, DltResetToFactoryDefaultRequest, \
    DltSetMessageFilteringRequest, DltGetSoftwareVersionRequest, \
    DltGetTraceStatusRequest
from dlt.constants import ServiceId, DltMessageType, DltControlType
from.payload import DltPayload


# prepare logger
log = logging.getLogger(__name__)


# deprecated services
DEPRECATED_SERVICES = [
    ServiceId.SET_COM_INTERFACE_STATUS,
    ServiceId.SET_COM_INTERFACE_MAX_BANDWIDTH,
    ServiceId.SET_VERBOSE_MODE,
    ServiceId.SET_TIMING_PACKETS,
    ServiceId.GET_LOCAL_TIME,
    ServiceId.SET_USE_ECU_ID,
    ServiceId.SET_USE_SESSION_ID,
    ServiceId.SET_USE_TIMESTAMP,
    ServiceId.SET_USE_EXTENDED_HEADER,
    ServiceId.MESSAGE_BUFFER_OVERFLOW,
    ServiceId.GET_COM_INTERFACE_STATUS,
    ServiceId.GET_COM_INTERFACE_MAX_BANDWIDTH,
    ServiceId.GET_VERBOSE_MODE_STATUS,
    ServiceId.GET_MESSAGE_FILTERING_STATUS,
    ServiceId.GET_USE_ECU_ID,
    ServiceId.GET_USE_SESSION_ID,
    ServiceId.GET_USE_TIMESTAMP,
    ServiceId.GET_USE_EXTENDED_HEADER
]

# mapping of service IDs to classes
SERVICE_CLS_MAPPING = {
    ServiceId.SET_DEFAULT_LOG_LEVEL: DltSetDefaultLogLevelRequest,
    ServiceId.SET_DEFAULT_TRACE_STATUS: DltSetDefaultTraceStatusRequest,
    ServiceId.GET_LOG_INFO: DltGetLogInfoRequest,
    ServiceId.GET_DEFAULT_LOG_LEVEL: DltSetDefaultLogLevelRequest,
    ServiceId.STORE_CONFIG: DltStoreConfigurationRequest,
    ServiceId.RESET_TO_FACTORY_DEFAULT: DltResetToFactoryDefaultRequest,
    ServiceId.SET_MESSAGE_FILTERING: DltSetMessageFilteringRequest,
    ServiceId.GET_SOFTWARE_VERSION: DltGetSoftwareVersionRequest,
    ServiceId.GET_TRACE_STATUS: DltGetTraceStatusRequest,
    # TODO: missing service types:
    #   GetLogChannelNames
    #   TraceStatus
    #   SetLogChannelAssignment
    #   SetLogChannelThreshold
    #   GetLogChannelThreshold
    #   BufferOverflowNotification
    #   CallSWCInjection
}


class DltPayloadNonVerbose(DltPayload):
    """
    non-verbose payload class
    """
    def type(self) -> DltPayloadType:
        """
        payload type

        :return: payload type
        :rtype: DltPayloadType
        """
        return DltPayloadType.NON_VERBOSE

    @classmethod
    def create_from(
        cls,
        f: BinaryIO,
        header: DltHeader
    ):
        obj = cls()

        # set msbf
        obj.msbf = header.standard.has_msbf()

        # enforce little endian
        tr = TypeReader(msbf=False)
        obj.message_id = tr.read_uint32(f)

        # read payload (size minus message ID)
        obj.value = f.read(header.payload_size() - 4)

        if header.extended is None:
            # no extended header found => just return the object
            return obj

        if header.extended.mstp == DltMessageType.CONTROL:
            # control message
            if header.extended.mtin == DltControlType.REQUEST:
                # requests
                try:
                    # get service class by the service ID
                    return SERVICE_CLS_MAPPING.get(
                        ServiceId(obj.message_id)
                    )

                except KeyError:
                    # service ID not defined in ServiceId enum
                    if obj.message_id in DEPRECATED_SERVICES:
                        # deprecated services
                        log.warning(
                            f"skipping deprecated service: "
                            f"{obj.message_id}"
                        )

                    else:
                        # not implemented
                        log.error(f"NOT IMPLEMENTED: {obj.message_id}")

                return None

        return obj

    def __repr__(self) -> str:
        """
        string representation of non-verbose payload

        :return: string representation of non-verbose payload
        :rtype: str
        """
        return (
            f"<DltPayloadNonVerbose(message_id=0x{self.message_id:02x}, "
            f"value={self.value})>"
        )

    def __str__(self) -> str:
        """
        string representation of the non-verbose payload value

        :return: non-verbose payload value
        :rtype: str
        """
        return (
            f"{self.value.decode('utf-8', errors='replace')} | {self.value.hex(' ')}"
        )
