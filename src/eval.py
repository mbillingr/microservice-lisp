import httpx
from typing import Any
from pydantic import BaseModel

from .config import APPLICATOR, EVALUATOR, GLOBAL_ENV
from .common import initialize_app


app = initialize_app("eval")


class Input(BaseModel):
    expr: Any
    env: dict[str, Any]


@app.post("/")
async def eval(input: Input) -> Any:
    async with httpx.AsyncClient() as client:
        match input.expr:
            case int(x): return x
            case str(x):
                if x in input.env:
                    return input.env[x]
                else:
                    response = await client.post(GLOBAL_ENV + "lookup", json={"key": x})
                    return response.json()
            case ["quote", x]: return x
            case ["let", [var, val], body]:
                response = await client.post(EVALUATOR, json={"expr": val, "env": input.env})
                val = response.json()
                response = await client.post(EVALUATOR, json={"expr": body, "env": input.env | {var: val}})
                return response.json()
            case ["if", test, conseq, alt]:
                response = await client.post(EVALUATOR, json={"expr": test, "env": input.env})
                branch = conseq if response.json() else alt
                response = await client.post(EVALUATOR, json={"expr": branch, "env": input.env})
                return response.json()
            case ["lambda", params, body]:
                return {"type": "function", "params": params, "body": body, "closure": input.env}
            case ["define", var, val]:
                response = await client.post(EVALUATOR, json={"expr": val, "env": input.env})
                val = response.json()
                await client.post(GLOBAL_ENV + "insert", json={"key": var, "value": val})
                return None
            case list():
                response = await client.post(APPLICATOR, json={"expr": input.expr, "env": input.env})
                return response.json()
            case _: raise SyntaxError(input.expr)