import re
import httpx
from typing import Any
from fastapi import Request
from .common import initialize_app
from .config import EVALUATOR

app = initialize_app("exec")


@app.post("/")
async def exec(request: Request) -> Any:
    src = await request.body()
    tokens = (parse_token(t) for t in re.split(b"([()']|\\s)", src) if t and not t.isspace())
    expr = parse_expr(tokens)

    async with httpx.AsyncClient() as client:
        response = await client.post(EVALUATOR, json={"expr": expr, "env": {}})
    return response.json()


def parse_token(t):
    try:
        return int(t)
    except ValueError:
        pass
    return t.decode()


def parse_expr(tokens):
    token = next(tokens)
    match token:
        case '(': return parse_list(tokens)
        case ')': raise ClosingParen()
        case "'": return ["quote", parse_expr(tokens)]
        case _: return token


def parse_list(tokens):
    expr = []
    try:
        while True:
            expr.append(parse_expr(tokens))
    except ClosingParen:
        return expr


class ClosingParen(Exception):
    pass

