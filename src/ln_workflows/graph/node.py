from abc import ABC, abstractmethod
from typing import Any, Self

from pydantic import (
    BaseModel,
    Field,
    ImportString,
)

from ln_workflows.graph.data import WorkflowData
from ln_workflows.io.input import WorkflowInput
from ln_workflows.io.result import WorkflowResult

# Abstract Classes


class WorkflowNode(ABC):
    def __init__(self, id: str, **kwargs: Any):
        self.id: str = id
        self.kwargs = kwargs

    def __hash__(self):
        return hash(self.id)

    def __call__(self, *args: Any, **kwargs: Any) -> Any: ...

    @classmethod
    def from_schema(cls, schema: "WorkflowNodeSchema") -> "WorkflowNode":
        return schema.source(id=schema.id, **schema.kwargs)


class WorkflowNodeSchema(BaseModel):
    id: str
    source: ImportString = Field(...)
    kwargs: dict[str, Any] = Field(...)
    
    @classmethod
    def from_obj(cls, obj: WorkflowNode) -> Self:
        obj_cls = obj.__class__
        return cls(id=obj.id, source=f"{obj_cls.__module__}.{obj_cls.__name__}", kwargs=obj.kwargs)


class WorkflowNodeIngress(WorkflowNode):
    @abstractmethod
    def __call__(self, i: WorkflowInput) -> dict[str, WorkflowData]: ...


class WorkflowNodeStep(WorkflowNode):
    @abstractmethod
    def __call__(self, **i: WorkflowData) -> dict[str, WorkflowData]: ...


class WorkflowNodeEgress(WorkflowNode):
    @abstractmethod
    def __call__(self, **i: WorkflowData) -> WorkflowResult: ...


# Implementations

class NoOp(WorkflowNodeStep):
    def __call__(self, **i: WorkflowData) -> dict[str, WorkflowData]:
        return i