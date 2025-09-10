from dataclasses import dataclass

from corbel import field
from corbel.mixins._hooks import HooksMixin


@dataclass
class Dummy(HooksMixin):
    x: int
    y: str
    _updates: list[str | int, ...] = field(default_factory=list)

    def _corbel_on_field_update(self, field, value, old_value):
        self._updates.append((field.name, old_value, value))


def test_hooks_trigger_on_update():
    d = Dummy(x=1, y="a")
    assert d._updates == []

    d.x = 10
    d.y = "b"

    assert d._updates == [("x", 1, 10), ("y", "a", "b")]


def test_hooks_do_not_trigger_before_initialized():
    class PreInitDummy(HooksMixin):
        x: int

        def __init__(self):
            self._updates = []

        def _corbel_on_field_update(self, field, value, old_value):
            self._updates.append((field.name, old_value, value))

    d = PreInitDummy()
    d.x = 5
    assert d._updates == []
