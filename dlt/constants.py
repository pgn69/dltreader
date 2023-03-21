from enum import Enum


# pattern that is required as start of each storage header
DLT_STORAGE_HEADER_PATTERN = "DLT\x01"


class DltStandardHeaderExtendedMask(Enum):
    """
    extended header mask
    """
    # verbose
    VERB = 0b00000001
    # message type
    MSTP = 0b00001110
    # message type info
    MTIN = 0b11110000


class DltStandardHeaderType(Enum):
    """
    header type
    """
    UEH = 0b00000001    # use extended header
    MSBF = 0b00000010   # True => Payload BigEndian else Payload LittleEndian
    WEID = 0b00000100   # with ECU ID
    WSID = 0b00001000   # with Session ID
    WTMS = 0b00010000   # with timestamp


class DltStandardHeaderExtendedFlags(Enum):
    """
    dlt standard header version flag
    """
    VERS = 0b11100000   # Version 1


class DltSize(Enum):
    """
    dlt sizes
    """
    WEID = 4
    WSID = 4
    WTMS = 4


class DltMessageType(Enum):
    """
    dlt types
    """
    LOG = 0x00
    APP_TRACE = 0x01
    NW_TRACE = 0x02
    CONTROL = 0x03


class DltLogLevelType(Enum):
    """
    dlt log level types
    """
    # fatal system error
    FATAL = 0x01
    # SWC error
    ERROR = 0x02
    # correct behavior cannot be ensured
    WARN = 0x03
    # log level type information
    INFO = 0x04
    # log level type debug
    DEBUG = 0x05
    # log level type verbose
    VERBOSE = 0x06


class DltAppTraceType(Enum):
    """
    dlt application trace types
    """
    # value of a variable
    VARIABLE = 0x01
    # call of a function
    FUNCTION_IN = 0x02
    # return of a function
    FUNCTION_OUT = 0x03
    # state of a state machine
    STATE = 0x04
    # RTE events
    VFB = 0x05


class DltControlType(Enum):
    """
    dlt control types
    """
    # request control message
    REQUEST = 0x01
    # response control message
    RESPONSE = 0x02


class DltNetworkTraceType(Enum):
    """
    dlt network trace types
    """
    # inter process communication
    IPC = 0x01
    # CAN communication bus
    CAN = 0x02
    # FlexRay communication bus
    FLEXRAY = 0x03
    # Most communication bus
    MOST = 0x04
    # Ethernet communication
    ETHERNET = 0x05
    # SOME/IP communication
    SOMEIP = 0x06


class DltPayloadType(Enum):
    """
    dlt payload type
    """
    NON_VERBOSE = 0x0
    VERBOSE = 0x01


class PayloadArgumentFlag(Enum):
    """
    payload argument flag
    """
    # bit type length
    TYLE = 0b00000000000000000000000000001000
    BOOL = 0b00000000000000000000000000010000
    SINT = 0b00000000000000000000000000100000
    UINT = 0b00000000000000000000000001000000
    FLOA = 0b00000000000000000000000010000000
    ARAY = 0b00000000000000000000000100000000
    STRG = 0b00000000000000000000001000000000
    RAWD = 0b00000000000000000000010000000000
    # bit variable info
    VARI = 0b00000000000000000000100000000000
    # bit fixed point
    FIXP = 0b00000000000000000001000000000000
    # trace info
    TRAI = 0b00000000000000000010000000000000
    # structured data
    STRU = 0b00000000000000000100000000000000
    SCOD = 0b00000000000000001000000000000000


class PayloadArgumentMask(Enum):
    """
    payload argument mask
    """
    TYLE = 0b00000000000000000000000000001111
    SCOD = 0b00000000000000111000000000000000


class ScodType(Enum):
    """
    scod types
    """
    ASCII = 0x00
    UTF8 = 0x01


class TyleType(Enum):
    """
    tyle types
    """
    UNDEFINED = 0x00
    BIT8 = 0x01
    BIT16 = 0x02
    BIT32 = 0x03
    BIT64 = 0x04
    BIT128 = 0x05


class TraceStatusType(Enum):
    """
    dlt trace status type
    """
    DEFAULT = -0x01
    OFF = 0x00
    ON = 0x01


class StatusType(Enum):
    """
    dlt status type
    """
    OFF = 0x00
    ON = 0x01


class ServiceId(Enum):
    """
    dlt service ID
    """
    # set the log Level
    SET_LOG_LEVEL = 0x01
    # enable/disable trace messages
    SET_TRACE_STATUS = 0x02
    # returns the log level for registered applications
    GET_LOG_INFO = 0x03
    # returns the log level for wildcards
    GET_DEFAULT_LOG_LEVEL = 0x04
    # stores the current configuration non volatile
    STORE_CONFIG = 0x05
    # sets the configuration back to default
    RESET_TO_FACTORY_DEFAULT = 0x06
    # set the com interface status (DEPRECATED)
    SET_COM_INTERFACE_STATUS = 0x07
    # set the com interface max bandwidth (DEPRECATED)
    SET_COM_INTERFACE_MAX_BANDWIDTH = 0x08
    # set verbose mode (DEPRECATED)
    SET_VERBOSE_MODE = 0x09
    # enable/disable message filtering
    SET_MESSAGE_FILTERING = 0x0a
    # set timing packets (DEPRECATED)
    SET_TIMING_PACKETS = 0x0b
    # get local time (DEPRECATED)
    GET_LOCAL_TIME = 0x0c
    # set use ecu id (DEPRECATED)
    SET_USE_ECU_ID = 0x0d
    # set use session id (DEPRECATED)
    SET_USE_SESSION_ID = 0x0e
    # set use timestamp (DEPRECATED)
    SET_USE_TIMESTAMP = 0x0f
    # set use extended header (DEPRECATED)
    SET_USE_EXTENDED_HEADER = 0x10
    # set the loglevel for wildcards
    SET_DEFAULT_LOG_LEVEL = 0x11
    # enable/disable trace messages for wildcards
    SET_DEFAULT_TRACE_STATUS = 0x12
    # get the ECU software version
    GET_SOFTWARE_VERSION = 0x13
    # message buffer overflow (DEPRECATED)
    MESSAGE_BUFFER_OVERFLOW = 0x14
    # get the current trace level for wildcards
    GET_DEFAULT_TRACE_STATUS = 0x15
    # get com interface status (DEPRECATED)
    GET_COM_INTERFACE_STATUS = 0x16
    # returns the log channel's name
    GET_LOG_CHANNEL_NAMES = 0x17
    # get com interface max bandwidth (DEPRECATED)
    GET_COM_INTERFACE_MAX_BANDWIDTH = 0x18
    # get verbose mode status (DEPRECATED)
    GET_VERBOSE_MODE_STATUS = 0x19
    # get message filtering status (DEPRECATED)
    GET_MESSAGE_FILTERING_STATUS = 0x1a
    # get use ecu id (DEPRECATED)
    GET_USE_ECU_ID = 0x1b
    # get use session id (DEPRECATED)
    GET_USE_SESSION_ID = 0x1c
    # get use timestamp (DEPRECATED)
    GET_USE_TIMESTAMP = 0x1d
    # get use extended header (DEPRECATED)
    GET_USE_EXTENDED_HEADER = 0x1e
    # returns the current trace status
    GET_TRACE_STATUS = 0x1f
    # adds/removes the given log channel as output path
    SET_LOG_CHANNEL_ASSIGNMENT = 0x20
    # sets the filter threshold for the given log channel
    SET_LOG_CHANNEL_THRESHOLD = 0x21
    # returns the current log level for a given log channel
    GET_LOG_CHANNEL_THRESHOLD = 0x22
    # report that a buffer overflow occurred
    BUFFER_OVERFLOW_NOTIFICATION = 0x23


class ServiceResponse(Enum):
    """
    dlt service response
    """
    OK = 0x00
    NOT_SUPPORTED = 0x01
    ERROR = 0x02
