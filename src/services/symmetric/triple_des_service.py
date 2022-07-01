from typing_extensions import Literal
from config.enums import TDESMode
from services.base_service import BaseService
from Crypto import Random
from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode


class TripleDESService(BaseService):
    def __init__(self, action: Literal["encrypt", "decrypt"], mode: Literal[tuple(TDESMode.get_value_dict().values())],
                 text, key=None):
        self.mode = mode
        self.action = action
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
        if self.mode in [DES3.MODE_ECB, DES3.MODE_CTR]:
            cipher = DES3.new(self.key, self.mode)
            encrypted_text = cipher.encrypt(plain_text.encode())
            return b64encode(encrypted_text).decode("utf-8"), self.key

        iv = Random.new().read(self.block_size)
        cipher = DES3.new(self.key, self.mode, iv)
        encrypted_text = cipher.encrypt(plain_text.encode())
        return b64encode(iv + encrypted_text).decode("utf-8"), self.key

    def decrypt(self, encrypted_text):
        encrypted_text = b64decode(encrypted_text)
        if self.mode in [DES3.MODE_ECB, DES3.MODE_CTR]:
            cipher = DES3.new(self.key, self.mode)
            plain_text = cipher.decrypt(encrypted_text).decode("utf-8")
            return self._unpad(plain_text)
        iv = encrypted_text[:self.block_size]
        cipher = DES3.new(self.key, self.mode, iv)
        plain_text = cipher.decrypt(encrypted_text[self.block_size:]).decode("utf-8")
        return self._unpad(plain_text)

    def validate(self):
        if self.key:
            self.key = b64decode(self.key)

        if self.key and len(self.key) not in DES3.key_size:
            self.add_error(message="Not a valid TDES key", fields=["key"])

    def pre_process(self):
        for k, v in TDESMode.get_value_dict().items():
            if v == self.mode:
                self.mode = k
                break

    def process(self):
        if self.action == "encrypt":
            encrypted_text, key = self.encrypt(self.text)
            return {
                "key": b64encode(key),
                "encrypted_text": encrypted_text
            }
        return self.decrypt(self.text)


if __name__ == "__main__":
    res = TripleDESService(action="encrypt", text="aaa", mode=TDESMode.MODE_CBC.description).execute()
    print(res)
    des_decrypted = TripleDESService(action="decrypt", text=res["encrypted_text"],
                                     mode=TDESMode.MODE_CBC.description,
                                     key=res["key"]).execute()
    print(des_decrypted)
