from dataclasses import field, dataclass

import pytest

from corbel.errors import DeserializeError


@dataclass
class Dummy:
    x: int = 0


def test_deserialize_error_attributes():
    f = field(default=0)
    val = "abc"
    orig_error = ValueError("bad value")
    err = DeserializeError("failed", field=f, value=val, error=orig_error)

    assert err.field == f
    assert err.value == val
    assert err.error == orig_error
    assert str(err) == "failed"


def test_deserialize_error_can_be_raised():
    val = 123
    with pytest.raises(DeserializeError) as excinfo:
        raise DeserializeError("oops", value=val)

    assert excinfo.value.value == val
    assert excinfo.value.field is None
    assert excinfo.value.error is None
    assert str(excinfo.value) == "oops"
