from abc import abstractmethod, ABC
from typing import List


class ServiceValidationError(Exception):
    def __init__(self, message, errors=None):
        super().__init__(message)
        self.errors = errors if errors is not None else []


class BaseService(ABC):
    def __init__(self, block_size):
        self.validation_errors = []
        self.process_time = None
        self.block_size = block_size

    def add_error(self, message: str, error_code: int = 0, fields: List = None):
        self.validation_errors.append({"message": message,
                                       "error_code": error_code,
                                       "fields": fields if fields is not None else []})

    def _pad(self, plain_text):
        number_of_bytes_to_pad = self.block_size - len(plain_text) % self.block_size
        ascii_string = chr(number_of_bytes_to_pad)
        padding_str = number_of_bytes_to_pad * ascii_string
        padded_plain_text = plain_text + padding_str
        return padded_plain_text

    @staticmethod
    def _unpad(plain_text):
        last_character = plain_text[len(plain_text) - 1:]
        return plain_text[:-ord(last_character)]

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
