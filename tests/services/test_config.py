import os
import pytest
import _pytest.monkeypatch

from typing import Iterator, List, Tuple, Mapping

from app.services.config import (
    EnvironmentConfigServiceBackend,
    ConfigServiceBackend,
    ConfigService,
)

# FIXME: use `pytest.mark.parameterize()`
class TestEnvironmentConfigServiceBackend:
    def test_get(self, monkeypatch: _pytest.monkeypatch.MonkeyPatch):
        monkeypatch.setenv("key", "value")
        backend = EnvironmentConfigServiceBackend()
        assert backend.get("key") == "value"
        assert backend.get("key") != "unexpected"

    def test_set(self):
        backend = EnvironmentConfigServiceBackend()
        backend.set("key", "value")
        assert os.environ["key"] == "value"


def _generate_backends() -> Iterator[Tuple[ConfigServiceBackend, Mapping[str, str]]]:
    backends: List[ConfigServiceBackend] = [EnvironmentConfigServiceBackend()]
    variables: Mapping[str, str] = {
        "key": "value",
    }

    return map(lambda x: _initialize_backend(x, variables), backends)


def _initialize_backend(
    backend: ConfigServiceBackend, variables: Mapping[str, str]
) -> Tuple[ConfigServiceBackend, Mapping[str, str]]:
    for key, value in variables.items():
        backend.set(key, value)

    return backend, variables


@pytest.mark.parametrize(["backend", "prestored_variables"], list(_generate_backends()))
class TestConfigService:
    def test_get(
        self, backend: ConfigServiceBackend, prestored_variables: Mapping[str, str]
    ):
        config = ConfigService(backend)
        for key, value in prestored_variables.items():
            assert config.get(key) == value

    def test_set(
        self,
        backend: ConfigServiceBackend,
        prestored_variables: Mapping[str, str],
    ):
        config = ConfigService(backend)
        for key, value in prestored_variables.items():
            new_value = key + value
            config.set(key, new_value)
            assert config.get(key) == new_value
            assert config.get(key) != value
