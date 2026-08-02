import os

from maggma.stores import MongoURIStore
from pydantic import TypeAdapter

from ln_workflows.schema import WorkflowResult


class WorkflowResultStore(MongoURIStore):
    def __init__(self, database: str = "ln_workflows", collection: str = "results"):
        self.uri = os.environ["MONGO_URI"]
        super().__init__(self.uri, collection_name=collection, database=database)

    def update_results(self, results: list[WorkflowResult]) -> None:
        self.connect(force_reset=False)
        serialized: list[dict] = TypeAdapter(list[WorkflowResult]).dump_python(
            results, mode="json"
        )
        self.update(serialized, key="_id")
