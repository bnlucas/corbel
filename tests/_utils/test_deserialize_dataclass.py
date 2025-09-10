from dataclasses import dataclass

import pytest

from corbel._utils._deserialize_dataclass import deserialize_dataclass
from corbel.errors import DeserializeError


@dataclass
class Simple:
    a: int
    b: str


class CorbelDummy:
    corbel_fields = [
        type("Field", (), {"name": "x", "type": int})(),
        type("Field", (), {"name": "y", "type": str})(),
    ]

    def __init__(self, x: int, y: str):
        self.x = x
        self.y = y


def dummy_deserialize_fn(value, typ):
    return typ(value)


def test_deserialize_dataclass_standard():
    data = {"a": "42", "b": "hello"}
    result = deserialize_dataclass(data, Simple, dummy_deserialize_fn)
    assert isinstance(result, Simple)
    assert result.a == 42
    assert result.b == "hello"


def test_deserialize_dataclass_corbel_from_dict():
    data = {"x": "10", "y": "world"}
    result = deserialize_dataclass(data, CorbelDummy, dummy_deserialize_fn)
    assert isinstance(result, CorbelDummy)
    assert result.x == 10
    assert result.y == "world"


def test_deserialize_dataclass_raises_error_on_non_dict():
    with pytest.raises(DeserializeError):
        deserialize_dataclass("not-a-dict", Simple, dummy_deserialize_fn)
