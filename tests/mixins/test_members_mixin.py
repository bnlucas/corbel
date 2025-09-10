from dataclasses import dataclass, field

from corbel.mixins._members import MembersMixin
from corbel.decorators import corbel_property


@dataclass
class Dummy(MembersMixin):
    a: int
    b: str
    _private: int = field(default=0)

    @corbel_property()
    def prop(self):
        return self.a * 2

    @property
    def normal_prop(self):
        return self.b.upper()


def test_corbel_fields_and_names():
    d = Dummy(a=1, b="x")
    fields = d.corbel_fields
    names = d.corbel_field_names

    assert set(f.name for f in fields) == {"a", "b", "_private"}
    assert names == {"a", "b", "_private"}


def test_corbel_properties_and_names():
    d = Dummy(a=1, b="x")
    props = d.corbel_properties
    names = d.corbel_property_names

    prop_names = {p.fget.__name__ for p in props if hasattr(p, "fget")}

    assert prop_names == {"prop", "normal_prop"}
    assert names == {"prop", "normal_prop"}


def test_corbel_members_filters():
    d = Dummy(a=1, b="x")
    members = d.corbel_members(include_properties=True, include_private=False)
    assert "a" in members
    assert "b" in members
    assert "prop" in members
    assert "_private" not in members

    members_priv = d.corbel_members(include_properties=True, include_private=True)
    assert "_private" in members_priv

    members_no_props = d.corbel_members(include_properties=False)
    assert "prop" not in members_no_props
    assert "normal_prop" not in members_no_props
    assert "a" in members_no_props


def test_corbel_member_names_filters():
    d = Dummy(a=1, b="x")

    names = d.corbel_member_names()
    assert names == {"a", "b", "prop", "normal_prop"}

    names_priv = d.corbel_member_names(include_private=True)
    assert "_private" in names_priv
