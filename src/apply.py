import asyncio
import functools

import httpx
from typing import Any
from pydantic import BaseModel

from .config import EVALUATOR
from .common import initialize_app


app = initialize_app("apply")


class Input(BaseModel):
    expr: list[Any]
    env: dict[str, Any]


@app.post("/")
async def eval(input: Input) -> Any:
    async with httpx.AsyncClient() as client:
        tasks = [client.post(EVALUATOR, json={"expr": x, "env": input.env}) for x in input.expr]
        responses = await asyncio.gather(*tasks)
        values = (r.json() for r in responses)
        match next(values):
            case {"type": "function", "params": params, "body": body, "closure": closure}:
                env = closure | dict(zip(params, values))
                response = await client.post(EVALUATOR, json={"expr": body, "env": env})
                return response.json()
            case {"type": "primitive", "value": "+"}: return sum(values)
            case {"type": "primitive", "value": "*"}: return functools.reduce(lambda a, b: a*b, values)
            case {"type": "primitive", "value": "-"}: return functools.reduce(lambda a, b: a-b, values, next(values))
            case {"type": "primitive", "value": "/"}: return functools.reduce(lambda a, b: a/b, values, next(values))
            case {"type": "primitive", "value": "="}: return next(values) == next(values)
            case {"type": "primitive", "value": "<"}: return next(values) < next(values)
            case {"type": "primitive", "value": ">"}: return next(values) > next(values)
            case _: raise NotImplementedError()
