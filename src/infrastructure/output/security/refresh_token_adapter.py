import hashlib
import secrets

from domain.spi.refresh_token_port import RefreshTokenPort


class RefreshTokenAdapter(RefreshTokenPort):
    def generate(self) -> str:
        return secrets.token_urlsafe(64)

    def digest(self, token: str) -> str:
        return hashlib.sha256(token.encode("utf-8")).hexdigest()
