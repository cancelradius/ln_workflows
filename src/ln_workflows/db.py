from maggma.stores import MongoStore
from monty.json import jsanitize

def add_results(results: dict, db_name: str = "ln_workflows", db_collection: str = "results") -> None:
    db = MongoStore(
        database=db_name,
        collection=db_collection,
        username=os.
        host="localhost",
        port=27017,
    )