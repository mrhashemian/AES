from services.base_service import BaseService
from Crypto.Hash import SHA1


class SHA1Service(BaseService):
    def __init__(self, text):
        self.text = text
        super().__init__()

    @staticmethod
    def encode(plain_text):
        hash_object = SHA1.new(data=plain_text.encode())
        return hash_object.digest()

    def validate(self):
        pass

    def process(self):
        return self.encode(self.text)


if __name__ == "__main__":
    sha1 = SHA1Service(text="aaa").execute()
    print(sha1)
