import os
import uuid
from datetime import UTC, datetime

from pydantic import (
    UUID4,
    BaseModel,
    ConfigDict,
    Field,
    PastDatetime,
    computed_field,
    field_validator,
)

USER = os.environ.get("USER") or "unknown"

class WorkflowResult(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        populate_by_name=True,
        serialize_by_alias=True,
    )
    id: UUID4 = Field(default_factory=uuid.uuid4, alias="_id")
    user: str = Field(default=USER)
    started: PastDatetime = Field(...)
    finished: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))

    @computed_field
    @property
    def walltime(self) -> float:
        return (self.finished - self.started).total_seconds()

    @field_validator("started", "finished")
    @classmethod
    def _tz_utc(cls, v: datetime) -> datetime:
        if v.tzinfo is None:
            return v.replace(tzinfo=UTC)
        return v.astimezone(UTC)
