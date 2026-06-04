from dataclasses import dataclass
from uuid import UUID


@dataclass
class Client:
    name: str
    email: str
    phone: str
    nit: str
    address: str
    id: UUID | None = None
