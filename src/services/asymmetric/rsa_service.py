from time import sleep
from services.base_service import BaseService
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from typing_extensions import Literal
from base64 import b64decode , b64encode


class RSAService(BaseService):
    def __init__(self, action: Literal["generate", "encrypt" , "decrypt"] , text=None , pv_key=None , pb_key=None , enc_session_key=None , nonce=None , tag=None , ciphertext=None ):
        self.text = text
        self.action = action
        self.pb_key = pb_key
        self.pv_key = pv_key
        self.enc_session_key = enc_session_key
        self.nonce = nonce
        self.tag = tag
        self.ciphertext = ciphertext
        super().__init__()

    @staticmethod
    def encrypt(pvkey , plain_text):
        # file_out = open("encrypted_data.bin", "wb")

        # recipient_key = RSA.import_key(open("receiver.pem").read())
        recipient_key = RSA.import_key(pvkey)
        session_key = get_random_bytes(16)

        # Encrypt the session key with the public RSA key
        cipher_rsa = PKCS1_OAEP.new(recipient_key)
        enc_session_key = cipher_rsa.encrypt(session_key)

        # Encrypt the data with the AES session key
        cipher_aes = AES.new(session_key, AES.MODE_EAX)
        ciphertext, tag = cipher_aes.encrypt_and_digest(plain_text.encode())
        # [file_out.write(x) for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext)]
        # file_out.close()
        return b64encode(enc_session_key).decode(), b64encode(cipher_aes.nonce).decode(), b64encode(tag).decode(), b64encode(ciphertext).decode()

    @staticmethod
    def decrypt(pbkey , enc_session_key, nonce, tag, ciphertext):
        # file_in = open("encrypted_data.bin", "rb")

        # private_key = RSA.import_key(open("private.pem").read())
        private_key = RSA.import_key(pbkey)

        # enc_session_key, nonce, tag, ciphertext = [file_in.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1)]

        # Decrypt the session key with the private RSA key
        cipher_rsa = PKCS1_OAEP.new(private_key)
        session_key = cipher_rsa.decrypt(b64decode(enc_session_key))

        # Decrypt the data with the AES session key
        cipher_aes = AES.new(session_key, AES.MODE_EAX, b64decode(nonce))
        data = cipher_aes.decrypt_and_verify(b64decode(ciphertext), b64decode(tag))
        return data.decode("utf-8")

    def generate(self):
        key = RSA.generate(2048)
        private_key = key.export_key()
        public_key = key.publickey().export_key()
        return private_key.decode(),public_key.decode()

    def validate(self):
        pass

    def pre_process(self):
        pass

    def process(self):
        if self.action == "generate":
            return self.generate()
        elif self.action == "encrypt":
            return self.encrypt(self.pv_key , self.text)
        else:
            return self.decrypt(self.pb_key,self.enc_session_key, self.nonce, self.tag, self.ciphertext)


if __name__ == "__main__":
    # RSAService(text="hi, i am seyyed").execute()
    # print(RSAService(action="generate").execute())
    pb = '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAsozwUa7Ju2vxe9pu/04/\nGupe3btDrTpMltcx1a1HyVwSQmmbfNUBMqsbZyoX/Gca3YrBnC3xZKJZdKR6puZj\ndVSa2kzgVxDC213ioFHHHTKntWC0xEVNKjlYfGSdGhthm4J6PutB5CWtME5OWCgr\n9CtlJ//iJ5WZt5MkQRFNUwvS32FnPUMtGcWcpEz5HLxRYDpIP6xCkDuPt7auFqUZ\n0gXPQ3UPlWgCusNph6hs2oYsyRgzjg7YuIh7JI78e4CfL1MDGs61fIBo77zLFGLT\nttO1LK8alXxQTzGAdNbu5k1abrakMFfS2/P7txdANc57IwLmescOjL4dBKyXyo8P\n1QIDAQAB\n-----END PUBLIC KEY-----'
    pv = '-----BEGIN RSA PRIVATE KEY-----\nMIIEpQIBAAKCAQEAsozwUa7Ju2vxe9pu/04/Gupe3btDrTpMltcx1a1HyVwSQmmb\nfNUBMqsbZyoX/Gca3YrBnC3xZKJZdKR6puZjdVSa2kzgVxDC213ioFHHHTKntWC0\nxEVNKjlYfGSdGhthm4J6PutB5CWtME5OWCgr9CtlJ//iJ5WZt5MkQRFNUwvS32Fn\nPUMtGcWcpEz5HLxRYDpIP6xCkDuPt7auFqUZ0gXPQ3UPlWgCusNph6hs2oYsyRgz\njg7YuIh7JI78e4CfL1MDGs61fIBo77zLFGLTttO1LK8alXxQTzGAdNbu5k1abrak\nMFfS2/P7txdANc57IwLmescOjL4dBKyXyo8P1QIDAQABAoIBABabom1RUrFU1mee\njantlC96CCeOx9+2D08VMfXyojGUoyo+GYZJqURrZoWeTpmyy3PMVz4JkjRyGx4a\nGn6qEuNfIllsXQahNG8W2PSATlQ73wDoHRNyC/aB+tqLWdodp/MLJyPy4W28OIzy\niVh/w6r/2KfjLlVhS6yzKKbFhFM0qCY6oLoV5swJtze41CvXsKzmfOMaJb2U58+j\nJaQn/EAkZOIwCVTEHkwQcg5gcShwT75xMwcb8BHQgduVhnVKPbq6qFy0l6lT0ybx\nactgSrsFQS7l4nFfvYONxtNq7lug95BULSIGoiz5Z2QZPWzZvOTPzFBGdTLrtZPM\nPsXqR8ECgYEAuiwiRFcFg5AEPbozon8q9I1d2G+iicCfjvUHW62h5KckcVzkE9HF\nNyTGBi/M8GXiQnobI3XrzeKQ5YSeYrAiiBi5p6VhbwqlRzvNA6sfzNclIBzW+mFf\nIoI1odIeuDOiorPX7Xye48gA6QsPl8tmgMgbQyeqM3NOtIgf6FNOZsECgYEA9YT4\nkY8b8HLLgTiwByIaaaGcp0sa00fjeFNZU7ZDscwNEpQBvzRLJB6R9RVgPWT6Knft\nlbn3/F39VSk/oQ661QBEaMhIh4RvjRFPOpaGDXlEvtflWZGTZDIGD8IQFrhdM5FS\nvcKrLSUBzNnWg2aVXbKouzFHB0e2fIAKgx07IhUCgYEAnuMjq6eJMSssM3JCtyBJ\nDMXJnfpIgcA/bMZ6LSgWzwpG8+kPTkrtQY7E4mrRQSny3EFSAAWX5fLDLt7sPdWM\n4xIXAJkIerhfLlg/NC5LyYqkSK/UWYPYqZ7vHtgxF4wZ9Tn/wtNk14nOHRYvjKEv\nLiGaAspLW/XA6hpzANh4RQECgYEAihs3O6HVpIbeZJz/n7OWSe8H0K8Vst2QXgH8\nkHNJVv0iKV4qMWT4E6RClCtnDIH9muAFPCD1FvfD5iCi0zUW8XQKBysKaXicyyx+\ndcVwOKoLepK1R5H05/qfoEOYiz8/5h8L/QRBB872WUX8PcP5p1A1S78nZjf3tcbM\nov5RYhUCgYEAugzkgydlQ99ffC/7qqmonHHmljLT7zsPrPClUodNhs6u39qv3fvp\n2lHeZtjiE8us7zyACtFhrmjd8DqSh0H7uXJ2k56tF3OjLmZNsDCPnWh6/rmr0EeD\nUGNnS9qr/7trb35olERxhRM6oeFhIm3KDmrC/IBf4JYX4vxBc2KzFhw=\n-----END RSA PRIVATE KEY-----'
    enc = RSAService(action="encrypt",pv_key=pb , text="give me your sight").execute()
    print(enc)
    print(RSAService(action="decrypt" , pb_key=pv , enc_session_key=enc[0] , nonce=enc[1] , tag=enc[2] , ciphertext=enc[3]).execute())