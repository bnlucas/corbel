import pytest
from dataclasses import field, Field
from corbel.errors import ValidationError


def test_validation_error_attributes():
    f: Field = field()
    val = 123
    original_error = ValueError("invalid")

    err = ValidationError("fail", field=f, value=val, error=original_error)

    assert err.field is f
    assert err.value == val
    assert err.error is original_error
    assert str(err) == "fail"


def test_validation_error_can_be_raised():
    f: Field = field()
    with pytest.raises(ValidationError) as excinfo:
        raise ValidationError("oops", field=f, value="bad", error=None)

    assert excinfo.value.field is f
    assert excinfo.value.value == "bad"
    assert excinfo.value.error is None
