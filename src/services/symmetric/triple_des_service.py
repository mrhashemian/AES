from typing_extensions import Literal
from services.base_service import BaseService
from Crypto import Random
from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode


class TripleDESService(BaseService):
    def __init__(self, mode: Literal["encrypt", "decrypt"], text, key=None):
        self.mode = mode
        self.text = text
        self.key = key
        super().__init__(block_size=DES3.block_size)

    def encrypt(self, plain_text):
        if not self.key:
            while True:
                try:
                    self.key = DES3.adjust_key_parity(get_random_bytes(24))
                    break
                except ValueError:
                    pass
        plain_text = self._pad(plain_text)
        iv = Random.new().read(self.block_size)
        cipher = DES3.new(self.key, DES3.MODE_CBC, iv)
        encrypted_text = cipher.encrypt(plain_text.encode())
        return b64encode(iv + encrypted_text).decode("utf-8"), self.key

    def decrypt(self, encrypted_text):
        encrypted_text = b64decode(encrypted_text)
        iv = encrypted_text[:self.block_size]
        cipher = DES3.new(self.key, DES3.MODE_CBC, iv)
        plain_text = cipher.decrypt(encrypted_text[self.block_size:]).decode("utf-8")
        return self._unpad(plain_text)

    def validate(self):
        pass

    def process(self):
        if self.mode == "encrypt":
            return self.encrypt(self.text)
        return self.decrypt(self.text)


if __name__ == "__main__":
    des_encrypted, key = TripleDESService(mode="encrypt", text="aaa").execute()
    print(des_encrypted, key)
    des_decrypted = TripleDESService(mode="decrypt", text=des_encrypted, key=key)
    print(des_decrypted.execute())
