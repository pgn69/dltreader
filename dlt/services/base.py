from abc import ABC


class BaseService(ABC):
    """
    abstract base class from which all services are derived
    """
    @classmethod
    def create_from(cls: "BaseService", data):
        """
        override this method based on type
        """
        obj = cls(data)

        return obj

    def __repr__(self):
        return f"<{self.__class__.__name__}({self.__dict__})"


class BaseRequest(BaseService):
    """
    base request class from which all requests are derived
    """


class BaseResponse(BaseService):
    """
    base response class from which all responses are derived
    """
    @classmethod
    def create_from(cls, data):
        obj = cls()

        obj.result = data[0]

        return obj
