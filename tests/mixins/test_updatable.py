from dataclasses import dataclass, Field
from typing import Any

from corbel import field
from corbel import Validated
from corbel.mixins._updatable import Updatable


@dataclass
class Dummy(Updatable):
    x: int
    y: str
    _private: int = 0


@dataclass
class WithProperty(Updatable):
    x: int
    y: int

    @property
    def total(self) -> int:
        return self.x + self.y


@dataclass
class ValidatedDummy(Validated, Updatable):
    x: int = field(validator=lambda v: v > 0)


def test_copy_creates_identical_instance():
    d = Dummy(x=1, y="a", _private=5)
    c = d.copy()

    assert c is not d
    assert c.x == d.x
    assert c.y == d.y
    assert c._private == d._private


def test_update_modifies_specified_fields():
    d = Dummy(x=1, y="a", _private=5)
    u = d.update(x=10, y="b")

    assert u.x == 10
    assert u.y == "b"
    assert u._private == 5

    assert d.x == 1
    assert d.y == "a"


def test_update_with_deepcopy_creates_independent_copy():
    d = Dummy(x=1, y="a", _private=5)
    u = d.update(use_deepcopy=True, x=99)

    assert u.x == 99
    assert u.y == d.y

    u.y = "changed"
    assert d.y == "a"


def test_batch_update_toggles_validation():
    @dataclass
    class U(Updatable):
        x: int = 0
        y: str = ""
        _calls: list[tuple[str, int]] = field(default_factory=list)

        def _corbel_on_field_update(
            self,
            field: Field,
            value: Any,
            old_value: Any,
        ) -> None:
            self._calls.append((field.name, value))

    u = U()

    with u.batch_update() as bu:
        bu.x = 10
        bu.y = "b"

    assert u._corbel_validation
    assert u._calls == [("x", 10), ("y", "b")]


def test_update_skips_properties():
    w = WithProperty(x=1, y=2)

    updated = w.update(x=3)

    assert updated.x == 3
    assert updated.y == 2
    assert updated.total == 5


def test_batch_update_with_validated_is_safe():
    v = ValidatedDummy(1)

    with v.batch_update() as vb:
        vb.x = 2

    assert v.x == 2
