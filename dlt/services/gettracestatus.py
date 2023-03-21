from .base import BaseRequest, BaseResponse


class DltGetTraceStatusRequest(BaseRequest):
    """
    DLT get trace status request
    """


class DltGetTraceStatusResponse(BaseResponse):
    """
    DLT get trace status response
    """
    @classmethod
    def create_from(cls, data):
        obj = BaseRequest.create_from(data=data)
        obj.trace_status = data[1]

        return obj
