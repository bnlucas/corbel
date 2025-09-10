from dataclasses import dataclass

from corbel.mixins import Corbel


@dataclass
class Dummy(Corbel):
    x: int
    y: str


def test_asdict_caching_and_refresh():
    d = Dummy(x=1, y="a")

    first = d.asdict()
    second = d.asdict()
    assert first == second

    refreshed = d.asdict(refresh=True)
    assert refreshed == first
    assert refreshed is not first


def test_dirty_fields_tracking():
    d = Dummy(x=1, y="a")
    assert d._corbel_dirty_fields == {}

    d._corbel_validation = False
    d.x = 10
    d.y = "b"

    assert "x" in d._corbel_dirty_fields
    assert "y" in d._corbel_dirty_fields


def test_initialized_flag():
    d = Dummy(x=1, y="a")
    assert d._corbel_initialized is True

    @dataclass
    class PreInit(Corbel):
        val: int = 0

        def __post_init__(self):
            super().__post_init__()
            self._hook_called = True

    p = PreInit()
    assert getattr(p, "_hook_called", False) is True
    assert p._corbel_initialized is True


def test_validation_toggle():
    d = Dummy(x=1, y="a")
    assert d._corbel_validation is True

    d._corbel_validation = False
    assert d._corbel_validation is False

    d._corbel_validation = True
    assert d._corbel_validation is True
