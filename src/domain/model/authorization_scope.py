from enum import Enum


class AuthorizationScope(Enum):
    DENIED = "denied"
    OWN = "own"
    ALL = "all"
