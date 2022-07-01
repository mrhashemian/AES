from services.base_service import BaseService
from Crypto.Hash import SHA256
from Crypto.Cipher import AES


class SHA2Service(BaseService):
    def __init__(self, text):
        self.text = text
        super().__init__(block_size=AES.block_size)

    @staticmethod
    def encode(plain_text):
        hash_object = SHA256.new(data=plain_text.encode())
        return hash_object.digest()

    def validate(self):
        pass

    def process(self):
        return self.encode(self.text)


if __name__ == "__main__":
    sha2 = SHA2Service(text="aaa").execute()
    print(sha2)
