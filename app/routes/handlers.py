import json

from flask import Response

__all__ = (
    "ping",
    "pull_request",
)

# FIXME: use `TypedDict`
def ping(data: dict) -> Response:
    return Response("", 200)


# FIXME: use `TypedDict`
def pull_request(data: dict) -> Response:
    action: str = data["action"]
    body: str = data["pull_request"]["body"]
    _process_pull_request(body)
    return Response(json.dumps(data), 200, {"Content-Type": "application/json"})


def _process_pull_request(body: str) -> None:
    # TODO: implement processing body
    ...
