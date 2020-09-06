import hmac
import hashlib

from flask import request, Request, Response
from werkzeug.exceptions import BadRequest
from os import environ
from app.services.config import ConfigService, EnvironmentConfigServiceBackend
from typing import Callable, Dict, List, NewType

__all__ = (
    "GitHubEventHandler",
    "webhook",
)

GitHubEventHandler = Callable[[dict], Response]


def _validate_signature(request: Request):
    # See https://docs.github.com/en/developers/webhooks-and-events/securing-your-webhooks
    # for implementation.

    backend = EnvironmentConfigServiceBackend()
    config = ConfigService(backend)

    request_signature = request.headers.get("X-Hub-Signature")
    if request_signature is None:
        raise BadRequest("There was no X-Hub-Signature.")

    try:
        secret_key = config.get("SECRET_KEY")
    except KeyError:
        print("SECRET_KEY seems not set")
    data: bytes = request.get_data()
    hexdigest: str = hmac.new(
        secret_key.encode("utf-8"), data, hashlib.sha1
    ).hexdigest()
    expected_signature = f"sha1={hexdigest}"

    if not hmac.compare_digest(request_signature, expected_signature):
        raise BadRequest("Wrong signature came.")


def webhook(request: Request = request) -> Response:
    _validate_signature(request)

    event: str = request.headers["X-GitHub-Event"]
    data: dict = request.get_json()

    handlers: Dict[str, GitHubEventHandler] = {}
    ignore: GitHubEventHandler = lambda x: Response("", 200)
    handler: GitHubEventHandler = handlers.get(event, ignore)

    return handler(data)
