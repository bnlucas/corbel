import dataclasses
import json

from corbel._utils._to_json import to_json
from corbel.enums import Include


@dataclasses.dataclass
class Dummy:
    a: int = 1
    b: str = "x"

    def corbel_members(self, include_properties=True, include_private=False):
        return {
            "a": self.__dataclass_fields__["a"],
            "b": self.__dataclass_fields__["b"],
        }


def test_to_json_basic():
    obj = Dummy()
    result = to_json(obj, Include.ALWAYS)
    parsed = json.loads(result)
    assert parsed["a"] == 1
    assert parsed["b"] == "x"


def test_to_json_with_wrapper():
    obj = Dummy()
    result = to_json(obj, Include.ALWAYS, wrapper="data")
    parsed = json.loads(result)
    assert "data" in parsed
    assert parsed["data"]["a"] == 1
    assert parsed["data"]["b"] == "x"


def test_to_json_respects_json_key_override(monkeypatch):
    obj = Dummy()

    def fake_corbel_metadata(member, path=None, default=None):
        if member.name == "a" and path == "json.key":
            return "override"
        return member.metadata.get("corbel", {}).get("json", {}).get(path, default)

    import corbel._utils._to_json as mod

    monkeypatch.setattr(mod, "corbel_metadata", fake_corbel_metadata)

    result = mod.to_json(obj, Include.ALWAYS)
    parsed = json.loads(result)
    assert "override" in parsed
    assert parsed["override"] == 1


def test_to_json_includes_only_requested_fields():
    @dataclasses.dataclass
    class DummySelective:
        x: int = 1
        y: int = 2
        z: int = 3

        def corbel_members(self, **kwargs):
            return {k: self.__dataclass_fields__[k] for k in self.__dataclass_fields__}

    obj = DummySelective()
    result = to_json(obj, Include.NON_NONE)
    parsed = json.loads(result)
    assert set(parsed.keys()) == {"x", "y", "z"}
