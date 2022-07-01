from typing_extensions import Literal

from config.enums import AESMode
from services.base_service import BaseService
from Crypto.Hash import SHA256
from Crypto import Random
from Crypto.Cipher import AES
from base64 import b64encode, b64decode


class AESService(BaseService):
    def __init__(self, key, action: Literal["encrypt", "decrypt"],
                 mode: Literal[tuple(AESMode.get_value_dict().values())], text):
        self.action = action
        self.mode = mode
        self.key = SHA256.new(data=key.encode()).digest()
        self.text = text
        super().__init__(block_size=AES.block_size)

    def encrypt(self, plain_text):
        plain_text = self._pad(plain_text)
        if self.mode in [AES.MODE_ECB, AES.MODE_CTR, AES.MODE_CCM, AES.MODE_OCB]:
            cipher = AES.new(self.key, self.mode)
            encrypted_text = cipher.encrypt(plain_text.encode())
            return b64encode(encrypted_text).decode("utf-8")

        iv = Random.new().read(self.block_size)
        cipher = AES.new(self.key, self.mode, iv)
        if self.mode == AES.MODE_SIV:
            encrypted_text = cipher.encrypt_and_digest(plain_text.encode())
            return b64encode(iv + encrypted_text[0]).decode("utf-8")
        encrypted_text = cipher.encrypt(plain_text.encode())
        return b64encode(iv + encrypted_text).decode("utf-8")

    def decrypt(self, encrypted_text):
        encrypted_text = b64decode(encrypted_text)
        if self.mode in [AES.MODE_ECB, AES.MODE_CTR, AES.MODE_CCM, AES.MODE_OCB]:
            cipher = AES.new(self.key, self.mode)
            plain_text = cipher.decrypt(encrypted_text).decode("utf-8")
            return self._unpad(plain_text)

        iv = encrypted_text[:self.block_size]
        cipher = AES.new(self.key, self.mode, iv)
        plain_text = cipher.decrypt(encrypted_text[self.block_size:]).decode("utf-8")
        return self._unpad(plain_text)

    def validate(self):
        pass

    def pre_process(self):
        for k, v in AESMode.get_value_dict().items():
            if v == self.mode:
                self.mode = k
                break

    def process(self):
        if self.action == "encrypt":
            return self.encrypt(self.text)
        return self.decrypt(self.text)


if __name__ == "__main__":
    aes_encrypt = AESService(key="39393", action="encrypt", text="aaa", mode=AESMode.MODE_ECB.description).execute()
    print(aes_encrypt)
    aes_decrypt = AESService(key="39393", action="decrypt", text=aes_encrypt,
                             mode=AESMode.MODE_ECB.description).execute()
    print(aes_decrypt)
