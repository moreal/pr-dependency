import abc
import os


__all__ = (
    "ConfigServiceBackend",
    "EnvironmentConfigServiceBackend",
    "ConfigService",
)


class ConfigServiceBackend(abc.ABC):
    @abc.abstractclassmethod
    def get(self, key: str) -> str:
        ...

    @abc.abstractclassmethod
    def set(self, key: str, value: str) -> None:
        ...


class EnvironmentConfigServiceBackend(ConfigServiceBackend):
    def __init__(self, environ: os._Environ = os.environ):
        self._environ = environ

    def get(self, key: str) -> str:
        return self._environ[key]

    def set(self, key: str, value: str) -> None:
        self._environ[key] = value


class ConfigService:
    def __init__(self, backend: ConfigServiceBackend):
        self._backend = backend

    def get(self, key: str) -> str:
        return self._backend.get(key)

    def set(self, key: str, value: str) -> None:
        self._backend.set(key, value)
