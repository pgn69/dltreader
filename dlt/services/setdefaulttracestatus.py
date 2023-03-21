from .base import BaseRequest, BaseResponse
from ..constants import TraceStatusType


class DltSetDefaultTraceStatusRequest(BaseRequest):
    """
    DLT set default trace status request
    """
    @classmethod
    def create_from(cls, data):
        obj = cls()

        obj.new_trace_status = TraceStatusType(data[0])

        return obj


class DltSetDefaultTraceStatusResponse(BaseResponse):
    """
    DLT set default trace status response
    """
