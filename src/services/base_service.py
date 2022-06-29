from abc import abstractmethod, ABC
from typing import List


class ServiceValidationError(Exception):
    def __init__(self, message, errors=None):
        super().__init__(message)
        self.errors = errors if errors is not None else []


class BaseService(ABC):
    def __init__(self, ):
        self.validation_errors = []
        self.process_time = None

    def add_error(self, message: str, error_code: int = 0, fields: List = None):
        self.validation_errors.append({"message": message,
                                       "error_code": error_code,
                                       "fields": fields if fields is not None else []})

    @abstractmethod
    def validate(self):
        pass

    def check_validations(self):
        if len(self.validation_errors) > 0:
            raise ServiceValidationError("service validation errors", self.validation_errors)

    def pre_process(self):
        pass

    @abstractmethod
    def process(self):
        pass

    def execute(self):
        self.validate()
        self.check_validations()
        self.pre_process()
        return self.process()
