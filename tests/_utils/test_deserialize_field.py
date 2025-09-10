from dataclasses import dataclass, field

import pytest

from corbel._utils._deserialize_field import deserialize_field
from corbel.errors import DeserializeError


@dataclass
class Dummy:
    a: int = field(metadata={"corbel": {"deserializer": lambda v, t: int(v)}})
    b: str = field(metadata={})


def test_deserialize_field_default():
    f = Dummy.__dataclass_fields__["b"]
    assert deserialize_field(f, "hello", str) == "hello"


def test_deserialize_field_custom_deserializer():
    f = Dummy.__dataclass_fields__["a"]
    assert deserialize_field(f, "42", int) == 42


def test_deserialize_field_raises_deserialize_error():
    f = Dummy.__dataclass_fields__["a"]

    with pytest.raises(DeserializeError) as excinfo:
        deserialize_field(f, "not-an-int", int)

    err = excinfo.value

    assert err.field == f
    assert err.value == "not-an-int"
    assert isinstance(err.error, Exception)
