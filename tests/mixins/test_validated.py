from dataclasses import dataclass

import pytest

from corbel import field
from corbel.errors import ValidationError
from corbel.mixins import Validated


def valid_int(value):
    return isinstance(value, int)


@dataclass
class ValidDummy(Validated):
    a: int = field(validator=valid_int)
    b: int = field(validator=valid_int)
    c: int | None = field(default=None, validator=valid_int, allow_none=True)
    d: int | None = field(default=None, validator=valid_int, allow_none=True)


@dataclass
class FieldUpdateDummy(Validated):
    a: int = field(validator=valid_int)
    b: int = field(validator=valid_int)
    c: int | None = field(default=None, validator=valid_int, allow_none=True)
    d: int | None = field(default=None, validator=valid_int, allow_none=True)


def test_post_init_validation_pass():
    obj = ValidDummy(a=1, b=1)
    assert obj.a == 1
    assert obj.b == 1


def test_field_update_validation():
    obj = FieldUpdateDummy(a=1, b=1, c=None, d=None)

    obj.a = 10
    assert obj.a == 10

    with pytest.raises(ValidationError):
        obj.b = "not-an-int"


def test_allow_none():
    obj = ValidDummy(a=1, b=1, c=None, d=None)
    assert obj.c is None
    assert obj.d is None
