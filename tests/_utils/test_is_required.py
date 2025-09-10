import dataclasses

from corbel._utils._is_required import is_required


def test_is_required_true():
    f = dataclasses.field()
    assert is_required(f) is True


def test_is_required_false_with_default():
    f = dataclasses.field(default=10)
    assert is_required(f) is False


def test_is_required_false_with_default_factory():
    f = dataclasses.field(default_factory=list)
    assert is_required(f) is False
