from uuid import UUID

from application.dto.response.client_response_dto import (  # type: ignore
    ClientResponseDto,  # type: ignore
)


class ClientResponseDtoBuilder:
    def __init__(self):
        self._id = UUID("f2edbd83-8ea3-4f95-bc4b-28d33e40f81d")
        self._name = "Acme Labs"
        self._email = "contact@example.com"
        self._phone = "3001234567"
        self._nit = "900123456"
        self._address = "Main Street 123"

    def build(self) -> ClientResponseDto:
        return ClientResponseDto(
            id=self._id,
            name=self._name,
            email=self._email,
            phone=self._phone,
            nit=self._nit,
            address=self._address,
        )
