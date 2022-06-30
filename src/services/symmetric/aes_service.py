from typing_extensions import Literal
from services.base_service import BaseService
from Crypto.Hash import SHA256
from Crypto import Random
from Crypto.Cipher import AES
from base64 import b64encode, b64decode


class AESService(BaseService):
    def __init__(self, key, mode: Literal["encrypt", "decrypt"], text):
        self.mode = mode
        self.key = SHA256.new(data=key.encode()).digest()
        self.text = text
        super().__init__(block_size=AES.block_size)

    def encrypt(self, plain_text):
        plain_text = self._pad(plain_text)
        iv = Random.new().read(self.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        encrypted_text = cipher.encrypt(plain_text.encode())
        return b64encode(iv + encrypted_text).decode("utf-8")

    def decrypt(self, encrypted_text):
        encrypted_text = b64decode(encrypted_text)
        iv = encrypted_text[:self.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        plain_text = cipher.decrypt(encrypted_text[self.block_size:]).decode("utf-8")
        return self._unpad(plain_text)

    def validate(self):
        pass

    def process(self):
        if self.mode == "encrypt":
            return self.encrypt(self.text)
        return self.decrypt(self.text)


if __name__ == "__main__":
    aes_encrypt = AESService(key="39393", mode="encrypt", text="aaa").execute()
    print(aes_encrypt)
    aes_decrypt = AESService(key="39393", mode="decrypt", text=aes_encrypt).execute()
    print(aes_decrypt)
