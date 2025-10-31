import hashlib
import hmac
import os
from cryptography.fernet import Fernet

class SecurityManager:
    def __init__(self, key_path="resources/salt.key"):
        self.key_path = key_path
        self.key = self._load_or_create_key()

    def _load_or_create_key(self):
        if os.path.exists(self.key_path):
            with open(self.key_path, "rb") as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            os.makedirs(os.path.dirname(self.key_path), exist_ok=True)
            with open(self.key_path, "wb") as f:
                f.write(key)
            return key

    def encrypt_data(self, data: bytes) -> bytes:
        f = Fernet(self.key)
        return f.encrypt(data)

    def decrypt_data(self, encrypted_ bytes) -> bytes:
        f = Fernet(self.key)
        return f.decrypt(encrypted_data)

    @staticmethod
    def secure_hash(data: str) -> str:
        return hashlib.sha256(data.encode()).hexdigest()

    @staticmethod
    def constant_time_compare(a: str, b: str) -> bool:
        return hmac.compare_digest(a, b)
