from functools import cached_property

from corbel.decorators import corbel_property
from corbel._objects import CorbelProperty
from corbel.mixins._meta import CorbelMeta


class Base(metaclass=CorbelMeta):
    @property
    def regular_prop(self):
        return "base"

    @cached_property
    def cached_prop(self):
        return 42

    @corbel_property()
    def corbel_prop(self):
        return "corbel"


class Child(Base):
    @property
    def child_prop(self):
        return "child"


def test_corbelmeta_collects_properties():
    base_props = Base.__corbel_properties__

    assert "regular_prop" in base_props
    assert "cached_prop" in base_props
    assert "corbel_prop" in base_props

    child_props = Child.__corbel_properties__

    assert "regular_prop" in child_props
    assert "cached_prop" in child_props
    assert "corbel_prop" in child_props
    assert "child_prop" in child_props

    assert isinstance(base_props["corbel_prop"], CorbelProperty)
    assert isinstance(child_props["cached_prop"], cached_property)
    assert isinstance(child_props["child_prop"], property)
