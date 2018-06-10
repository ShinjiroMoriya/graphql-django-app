from cryptography.fernet import Fernet
from urllib.parse import quote, unquote
from django.conf import settings


class FernetCipher:
    def __init__(self):
        self.key = settings.FERNET_KEY
        self.f = Fernet(self.key.encode('utf-8'))

    def encrypt(self, raw):
        try:
            raw = raw.encode('utf-8')
            hashed = self.f.encrypt(raw)
            return quote(hashed.decode('utf-8').strip('=='))
        except:
            return ''

    def decrypt(self, enc):
        try:
            enc = unquote(enc) + '=='
            enc = enc.encode('utf-8')
            decrypted = self.f.decrypt(enc)
            return decrypted.decode('utf-8')
        except:
            return ''


fernet = FernetCipher()
