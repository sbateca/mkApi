from application.dto.request.create_client_request_dto import (  # type: ignore
    ClientRequestDto,
)


class CreateClientRequestDtoBuilder:
    def __init__(self):
        self._name = "Acme Labs"
        self._email = "contact@example.com"
        self._phone = "3001234567"
        self._nit = "900123456"
        self._address = "Main Street 123"

    def with_name(self, value: str) -> "CreateClientRequestDtoBuilder":
        self._name = value
        return self

    def with_email(self, value: str) -> "CreateClientRequestDtoBuilder":
        self._email = value
        return self

    def with_phone(self, value: str) -> "CreateClientRequestDtoBuilder":
        self._phone = value
        return self

    def with_nit(self, value: str) -> "CreateClientRequestDtoBuilder":
        self._nit = value
        return self

    def with_address(self, value: str) -> "CreateClientRequestDtoBuilder":
        self._address = value
        return self

    def build(self) -> ClientRequestDto:
        return ClientRequestDto(
            name=self._name,
            email=self._email,
            phone=self._phone,
            nit=self._nit,
            address=self._address,
        )

    def build_dict(self) -> dict[str, str]:
        return self.build().model_dump()
