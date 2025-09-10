import dataclasses

from dataclasses import dataclass

from corbel._utils._fields import fields


@dataclass
class Dummy:
    a: int
    b: str


class CorbelDummy:
    corbel_fields = (
        dataclasses.field(default=1),
        dataclasses.field(default="x"),
    )


def test_fields_returns_dataclass_fields_for_regular_class():
    flds = fields(Dummy)
    assert all(isinstance(f, dataclasses.Field) for f in flds)
    names = tuple(f.name for f in flds)
    assert "a" in names
    assert "b" in names


def test_fields_returns_corbel_fields_when_present():
    flds = fields(CorbelDummy)
    assert flds == CorbelDummy.corbel_fields
