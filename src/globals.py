from typing import Any

from pydantic import BaseModel
from .common import initialize_app


app = initialize_app("globals")


class Lookup(BaseModel):
    key: str


@app.post("/lookup")
async def lookup(input: Lookup) -> Any:
    return ENV[input.key]


class Insert(BaseModel):
    key: str
    value: Any


@app.post("/insert")
async def insert(input: Insert) -> None:
    ENV[input.key] = input.value

# Note that the process-local in-memory environment prevents us from scaling this service horizontally!
ENV = {
    "+": {"type": "primitive", "value": "+"},
    "-": {"type": "primitive", "value": "-"},
    "*": {"type": "primitive", "value": "*"},
    "/": {"type": "primitive", "value": "/"},
    "=": {"type": "primitive", "value": "="},
    "<": {"type": "primitive", "value": "<"},
    ">": {"type": "primitive", "value": ">"},
}
