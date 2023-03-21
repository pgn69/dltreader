from .base import BaseRequest, BaseResponse


class DltGetDefaultLogLevelRequest(BaseRequest):
    """
    DLT get default log level request
    """


class DltGetDefaultLogLevelResponse(BaseResponse):
    """
    DLT get default log level response
    """
    @classmethod
    def create_from(cls, data):
        obj = BaseRequest.create_from(data=data)
        obj.log_level = data[1]

        return obj
