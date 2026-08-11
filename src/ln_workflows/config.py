import json
from pathlib import Path
from typing import Any, Self

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    @classmethod
    def from_file(cls, file: Path | str) -> Self:
        with open(file, "r") as f:
            deserialized = json.load(f)
        config = cls(**deserialized)
        return config

    def to_file(self, file: Path | str) -> None:
        with open(file, "w") as f:
            f.write(self.model_dump_json(indent=2))
