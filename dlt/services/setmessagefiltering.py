from .base import BaseRequest, BaseResponse
from ..constants import StatusType


class DltSetMessageFilteringRequest(BaseRequest):
    """
    DLT set message filtering request
    """
    @classmethod
    def create_from(cls, data):
        obj = cls()

        obj.new_status = StatusType(data[0])

        return obj


class DltSetMessageFilteringResponse(BaseResponse):
    """
    DLT set message filtering response
    """
