from pydantic.dataclasses import dataclass


@dataclass(frozen=True)
class ActionDecision:
    allowed: bool
    code: str | None = None
    reason: str | None = None
