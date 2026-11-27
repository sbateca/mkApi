from pydantic import BaseModel

from domain.model.action_decision import ActionDecision


class ActionDecisionResponseDto(BaseModel):
    allowed: bool
    code: str | None = None
    reason: str | None = None

    @classmethod
    def from_decision(cls, decision: ActionDecision) -> "ActionDecisionResponseDto":
        return cls(allowed=decision.allowed, code=decision.code, reason=decision.reason)


class ResourceActionsResponseDto(BaseModel):
    actions: dict[str, ActionDecisionResponseDto]


class CollectionActionsResponseDto(BaseModel):
    create: ActionDecisionResponseDto
