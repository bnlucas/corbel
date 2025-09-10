import pytest
from corbel.errors import InclusionError


def test_inclusion_error_attributes():
    rule = "NON_NONE"
    err = InclusionError("invalid inclusion", include=rule)

    assert err.include == rule
    assert str(err) == "invalid inclusion"


def test_inclusion_error_can_be_raised():
    rule = "NON_EMPTY"
    with pytest.raises(InclusionError) as excinfo:
        raise InclusionError("oops", include=rule)

    assert excinfo.value.include == rule
    assert str(excinfo.value) == "oops"
