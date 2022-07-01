from services.base_service import BaseService
from Crypto.Hash import HMAC, SHA1,SHA256,SHA512,SHA3_256,SHA3_512
from typing_extensions import Literal

class HMACSercice(BaseService):
    def __init__(self, action: Literal["encode", "verify"] , secret , digestmod: Literal["SHA1","SHA256","SHA512","SHA3_256","SHA3_512"] , plain_text , hashed_text=None):
        self.action = action
        self.secret = secret
        if digestmod == "SHA1":
            self.digestmod = SHA1
        elif digestmod == "SHA256":
            self.digestmod = SHA256
        elif digestmod == "SHA512":
            self.digestmod = SHA512
        elif digestmod == "SHA3_256":
            self.digestmod = SHA3_256
        elif digestmod == "SHA3_512":
            self.digestmod = SHA3_512
        self.plain_text = plain_text
        self.hashed_text = hashed_text
        super().__init__()

    def encode(self):
        hash_object = HMAC.new(self.secret.encode() , digestmod= self.digestmod , msg=self.plain_text.encode())
        return hash_object.hexdigest()

    def verify(self):
        hash_object = HMAC.new(self.secret.encode() , digestmod= self.digestmod , msg=self.plain_text.encode())
        try:
            hash_object.hexverify(self.hashed_text)
            return "true"
        except:
            return "false"

    def validate(self):
        pass

    def process(self):
        if self.action == "encode":
            return self.encode()
        return self.verify()

if __name__ == "__main__":
    print(HMACSercice(action="encode", secret="seccc", digestmod="SHA1", plain_text="HPD").execute())
    print(HMACSercice(action="verify", secret="seccc", digestmod="SHA1", plain_text="HPD",hashed_text="4bbb6d7b434255a73baca9786ce14c35f716e8a7").execute())