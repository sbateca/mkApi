import base64
import hashlib

import bcrypt

from domain.spi.password_hasher_port import PasswordHasherPort


class BcryptPasswordHasher(PasswordHasherPort):
    def __init__(self, rounds: int = 12):
        self.rounds = rounds

    def hash(self, password: str) -> str:
        password_bytes = self._encode_password(password)
        return bcrypt.hashpw(password_bytes, bcrypt.gensalt(self.rounds)).decode(
            "utf-8"
        )

    def verify(self, password: str, password_hash: str) -> bool:
        try:
            return bcrypt.checkpw(
                self._encode_password(password),
                password_hash.encode("utf-8"),
            )
        except ValueError:
            return False

    @staticmethod
    def _encode_password(password: str) -> bytes:
        digest = hashlib.sha256(password.encode("utf-8")).digest()
        return base64.b64encode(digest)
