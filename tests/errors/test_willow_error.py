import pytest

from corbel.errors import CorbelError


def test_corbel_error_is_exception():
    err = CorbelError("oops")
    assert isinstance(err, Exception)
    assert str(err) == "oops"


def test_corbel_error_can_be_raised():
    with pytest.raises(CorbelError, match="fail"):
        raise CorbelError("fail")
