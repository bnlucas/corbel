import dataclasses

from corbel._utils._to_dict import to_dict
from corbel.enums import Include
from corbel.decorators import corbel_property


@dataclasses.dataclass
class Dummy:
    a: int = 1
    b: str = "x"

    def corbel_members(self, include_properties=True, include_private=False):
        return {
            "a": self.__dataclass_fields__["a"],
            "b": self.__dataclass_fields__["b"],
        }


def test_to_dict_includes_all_fields_by_default():
    obj = Dummy()
    result = to_dict(obj, Include.ALWAYS)
    assert result["a"] == 1
    assert result["b"] == "x"


def test_to_dict_respects_include_non_none():
    obj = Dummy(a=None)
    result = to_dict(obj, Include.NON_NONE)
    assert "a" not in result
    assert result["b"] == "x"


def test_to_dict_respects_custom_serializer_on_field():
    def serializer(val):
        return f"serialized-{val}"

    @dataclasses.dataclass
    class DummyFieldSerializer:
        x: int = dataclasses.field(
            default=10, metadata={"corbel": {"serializer": serializer}}
        )

        def corbel_members(self, **kwargs):
            return {"x": self.__dataclass_fields__["x"]}

    obj = DummyFieldSerializer()
    result = to_dict(obj, Include.ALWAYS)
    assert result["x"] == "serialized-10"


def test_to_dict_respects_custom_serializer_on_property():
    class DummyPropSerializer:
        @corbel_property()
        def x(self):
            return 42

        def corbel_members(self, include_properties=True, **kwargs):
            members = {}
            if include_properties:
                members["x"] = type(self).x
            return members

    setattr(
        DummyPropSerializer.x, "__corbel__", {"serializer": lambda v: f"serialized-{v}"}
    )

    obj = DummyPropSerializer()
    result = to_dict(obj, Include.ALWAYS)
    assert result["x"] == "serialized-42"


def test_to_dict_ignores_fields_marked_ignore():
    @dataclasses.dataclass
    class DummyIgnore:
        y: int = dataclasses.field(default=5, metadata={"corbel": {"ignore": True}})

        def corbel_members(self, **kwargs):
            return {"y": self.__dataclass_fields__["y"]}

    obj = DummyIgnore()
    result = to_dict(obj, Include.ALWAYS)
    assert "y" not in result
