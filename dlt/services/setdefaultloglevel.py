from .base import BaseRequest, BaseResponse
from ..constants import DltLogLevelType


class DltSetDefaultLogLevelRequest(BaseRequest):
    """
    DLT set default log level request
    """
    @classmethod
    def create_from(cls, data):
        obj = cls()

        obj.new_log_level = DltLogLevelType(data[0])

        return obj


class DltSetDefaultLogLevelResponse(BaseResponse):
    """
    DLT set default log level response
    """
