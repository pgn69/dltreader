from .base import BaseService


class DltResetToFactoryDefaultRequest(BaseService):
    """
    DLT reset to factor default request
    """


class DltResetToFactoryDefaultResponse(BaseService):
    """
    DLT reset to factor default response
    """
    @classmethod
    def create_from(cls, data):
        obj = cls()

        obj.len = int(data[:2])
        obj.sw_version = data[2:]

        return obj
