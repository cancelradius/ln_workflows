import os
from pathlib import Path

from maggma.stores import FileStore, MongoURIStore
from pydantic import TypeAdapter

from ln_workflows.io.result import WorkflowResult


class WorkflowInputStore(FileStore):
    def __init__(self, path: Path | str, **kwargs):
        super().__init__(path, **kwargs)

    def _index(self):
        with self as store:
            store.query()


class WorkflowResultStore(MongoURIStore):
    def __init__(self, database: str = "ln_workflows", collection: str = "results"):
        # TODO: define MONGO_URI with pydantic-settings config
        self.uri = os.environ.get("MONGO_URI")
        if not self.uri:
            raise RuntimeError(
                "Environment variable MONGO_URI is not set!"
            )
        super().__init__(self.uri, collection_name=collection, database=database, key="_id")

    def update_results(self, results: list[WorkflowResult]) -> None:
        serialized: list[dict] = TypeAdapter(list[WorkflowResult]).dump_python(
            results, mode="python"
        )
        self.update(serialized)
