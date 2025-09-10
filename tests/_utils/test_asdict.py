import dataclasses

from corbel._utils._asdict import asdict


@dataclasses.dataclass
class Simple:
    x: int = 1
    y: str = "a"

    def corbel_members(self, include_properties=True, include_private=False):
        return {
            "x": self.__dataclass_fields__["x"],
            "y": self.__dataclass_fields__["y"],
        }


def test_asdict_basic():
    obj = Simple()
    result = asdict(obj)
    assert result["x"] == 1
    assert result["y"] == "a"


def test_asdict_includes_private(monkeypatch):
    @dataclasses.dataclass
    class WithPrivate:
        _hidden: int = 99
        public: int = 1

        def corbel_members(self, include_properties=True, include_private=False):
            members = {"public": self.__dataclass_fields__["public"]}
            if include_private:
                members["_hidden"] = self.__dataclass_fields__["_hidden"]
            return members

    obj = WithPrivate()
    result = asdict(obj, include_private=True)
    assert result["_hidden"] == 99
    assert result["public"] == 1


def test_asdict_includes_properties():
    @dataclasses.dataclass
    class WithProp:
        x: int = 10

        @property
        def y(self):
            return self.x * 2

        def corbel_members(self, include_properties=True, include_private=False):
            members = {"x": self.__dataclass_fields__["x"]}
            if include_properties:
                members["y"] = type(self).y
            return members

    obj = WithProp()
    result = asdict(obj)
    assert result["x"] == 10
    assert result["y"] == 20


def test_asdict_nested_dataclass():
    @dataclasses.dataclass
    class Inner:
        a: int = 5

        def corbel_members(self, **kwargs):
            return {"a": self.__dataclass_fields__["a"]}

    @dataclasses.dataclass
    class Outer:
        inner: Inner

        def corbel_members(self, **kwargs):
            return {"inner": self.__dataclass_fields__["inner"]}

    outer = Outer(inner=Inner())
    result = asdict(outer)
    assert isinstance(result["inner"], dict)
    assert result["inner"]["a"] == 5
