import dataclasses

from corbel._utils._resolve_field_key import resolve_field_key


@dataclasses.dataclass
class Dummy:
    z: int = dataclasses.field(
        metadata={"corbel": {"json": {"key": "x", "aliases": ["y"]}}}
    )


def test_resolve_field_key_uses_json_key_if_present():
    f = dataclasses.field(metadata={"corbel": {"json": {"key": "a"}}})
    data = {"a": 10, "b": 20}
    assert resolve_field_key(f, data) == "a"


def test_resolve_field_key_uses_alias_if_key_missing():
    f = dataclasses.field(
        metadata={"corbel": {"json": {"key": "missing", "aliases": ["b", "c"]}}}
    )
    data = {"b": 2, "c": 3}
    assert resolve_field_key(f, data) == "b"


def test_resolve_field_key_converts_string_alias_to_list():
    f = dataclasses.field(metadata={"corbel": {"json": {"aliases": "b"}}})
    data = {"b": 5}
    assert resolve_field_key(f, data) == "b"


def test_resolve_field_key_falls_back_to_field_name():
    data = {"other": 1}
    f = Dummy.__dataclass_fields__["z"]
    assert resolve_field_key(f, data) == "z"


def test_resolve_field_key_with_empty_json_metadata():
    f = dataclasses.field(metadata={"corbel": {}})
    data = {"x": 1}
    assert resolve_field_key(f, data) == f.name
