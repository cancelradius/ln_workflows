import os
import uuid
from datetime import datetime, timedelta

from pydantic import UUID4, BaseModel, ConfigDict, Field, computed_field

USER = os.environ.get("USER") or "unknown"
PL_DATETIME = datetime.fromordinal(1)

class WorkflowResult(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        populate_by_name=True,
        serialize_by_alias=True,
    )
    id: UUID4 = Field(default_factory=uuid.uuid4, alias="_id")
    user: str = Field(default=USER)
    started: datetime = Field(default=PL_DATETIME)
    finished: datetime = Field(default_factory=datetime.now)

    @computed_field
    @property
    def walltime(self) -> timedelta:
        return self.finished - self.started
