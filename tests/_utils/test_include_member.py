from dataclasses import dataclass, field, Field

import pytest

from corbel._utils._default_value import default_value
from corbel._utils._include_member import include_member
from corbel.enums import Include
from corbel.errors import InclusionError
from corbel.types import Member


@dataclass
class Dummy:
    a: int = 10
    b: str = "x"
    c: list = field(default_factory=list)


def test_include_always():
    for val in [None, 0, "", [], {}]:
        f: Member = Dummy.__dataclass_fields__["a"]
        assert include_member(f, val, Include.ALWAYS) is True


def test_include_non_none():
    f: Member = Dummy.__dataclass_fields__["a"]
    assert include_member(f, 5, Include.NON_NONE) is True
    assert include_member(f, None, Include.NON_NONE) is False


def test_include_non_empty():
    f: Member = Dummy.__dataclass_fields__["b"]
    assert include_member(f, "text", Include.NON_EMPTY) is True
    assert include_member(f, "", Include.NON_EMPTY) is False
    assert include_member(f, [1], Include.NON_EMPTY) is True
    assert include_member(f, [], Include.NON_EMPTY) is False
    assert include_member(f, None, Include.NON_EMPTY) is False

    # Non-collection/truthy value
    class Obj:
        pass

    assert include_member(f, Obj(), Include.NON_EMPTY) is True


def test_include_non_default_field():
    f: Field = Dummy.__dataclass_fields__["a"]
    default_val = default_value(f)
    assert include_member(f, default_val, Include.NON_DEFAULT) is False
    assert include_member(f, default_val + 1, Include.NON_DEFAULT) is True


def test_include_non_default_property_raises():
    class DummyProp:
        @property
        def prop(self):
            return 5

    member: Member = DummyProp.prop
    with pytest.raises(InclusionError):
        include_member(member, 5, Include.NON_DEFAULT)


def test_include_unknown_rule_raises():
    f: Field = Dummy.__dataclass_fields__["a"]

    class FakeInclude:
        pass

    with pytest.raises(InclusionError):
        include_member(f, 1, FakeInclude())
