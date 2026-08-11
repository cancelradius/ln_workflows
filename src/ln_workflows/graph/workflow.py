from pathlib import Path
from typing import Any, Self

from networkx import MultiDiGraph, node_link_data, node_link_graph
from pydantic import BaseModel, Field

from ln_workflows.config import Config
from ln_workflows.graph.node import WorkflowNode, WorkflowNodeSchema


class Workflow(MultiDiGraph):
    def __init__(self, node_link_data: dict[str, list] | None = None, **globals: Any):
        if node_link_data is None:
            node_link_data = GraphSchema().model_dump()
        else:
            GraphSchema.model_validate(node_link_data)
        super().__init__(
            node_link_graph(node_link_data, directed=True, multigraph=True)
        )
        self.globals = globals

    @classmethod
    def from_file(cls, path: Path | str) -> Self:
        config = WorkflowConfig.from_file(path)
        return cls.from_config(config)

    @classmethod
    def from_config(cls, config: "WorkflowConfig") -> Self:
        return cls(node_link_data=config.graph.model_dump(), **config.globals)
    
    @classmethod
    def from_graph(cls, graph: MultiDiGraph, **globals: Any) -> Self:
        return cls(node_link_data=node_link_data(graph), **globals)

    def add_node(self, node_for_adding: WorkflowNode, **kwargs):
        schema = WorkflowNodeSchema.from_obj(node_for_adding)
        super().add_node(schema.id, **schema.model_dump(mode='json', exclude={'id',}))


class GraphSchema(BaseModel):
    nodes: list[WorkflowNodeSchema] = Field(default_factory=list)
    edges: list["EdgeSchema"] = Field(default_factory=list)


class EdgeSchema(BaseModel):
    source: str = Field(...)
    target: str = Field(...)
    key: str = Field(...)


class WorkflowConfig(Config):
    graph: GraphSchema = Field(default_factory=GraphSchema)
    globals: dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def from_obj(cls, obj: Workflow) -> Self:
        return cls(
            graph=GraphSchema.model_validate(node_link_data(obj)),
            globals=obj.globals,
        )


class WorkflowConfigStore(dict):
    def __init__(self, node_defs: dict[str, "WorkflowConfig"]):
        super().__init__(node_defs)

    @classmethod
    def from_directory(cls, directory: Path | str) -> "WorkflowConfigStore":
        wf_defs: dict[str, WorkflowConfig] = {}
        for wf_file in Path(directory).iterdir():
            if wf_file.is_file() and wf_file.suffix == ".json":
                wf_defs[wf_file.stem] = WorkflowConfig.from_file(wf_file)
        return cls(wf_defs)
