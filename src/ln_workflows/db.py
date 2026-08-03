import os

from maggma.stores import MongoURIStore
from pydantic import TypeAdapter

from ln_workflows.schema import WorkflowResult


class WorkflowResultStore(MongoURIStore):
    def __init__(self, database: str = "ln_workflows", collection: str = "results"):
        self.uri = os.environ.get("MONGO_URI")
        if not self.uri:
            raise RuntimeError(
                "Environment variable MONGO_URI is not set! This shouldn't happen, and probably means the container wasn't started correctly."
            )
        super().__init__(self.uri, collection_name=collection, database=database, key="_id")

    def update_results(self, results: list[WorkflowResult]) -> None:
        self.connect()
        serialized: list[dict] = TypeAdapter(list[WorkflowResult]).dump_python(
            results, mode="python"
        )
        self.update(serialized)
