from uuid import UUID

from pydantic import BaseModel


class ClientResponseDto(BaseModel):
    id: UUID | None
    name: str
    email: str
    phone: str
    nit: str
    address: str
