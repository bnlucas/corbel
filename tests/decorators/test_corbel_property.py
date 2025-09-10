import pytest
from corbel.decorators._property import corbel_property
from corbel._objects import CorbelProperty


class Dummy:
    def __init__(self):
        self._x = 10

    @corbel_property(json={"key": "value"}, allow_none=True)
    def x(self):
        return self._x

    @x.setter
    def x(self, val):
        self._x = val

    @x.deleter
    def x(self):
        del self._x


def test_corbel_property_metadata():
    prop = Dummy.x
    assert isinstance(prop, CorbelProperty)
    assert prop.__corbel__["json"] == {"key": "value"}
    assert prop.__corbel__["allow_none"] is True
    assert prop.__corbel__["ignore"] is False


def test_getter_setter_deleter():
    d = Dummy()
    assert d.x == 10

    d.x = 42
    assert d.x == 42

    del d.x
    with pytest.raises(AttributeError):
        _ = d.x
