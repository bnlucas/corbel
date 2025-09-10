import dataclasses

from corbel._utils._corbel_metadata import corbel_metadata
from corbel.decorators import corbel_property


def test_corbel_metadata_returns_full_dict_for_field():
    f = dataclasses.field(metadata={"corbel": {"foo": 123}})
    assert corbel_metadata(f) == {"foo": 123}


def test_corbel_metadata_returns_full_dict_for_property():
    class Dummy:
        @corbel_property(ignore=False)
        def prop(self):
            return 5

    p = Dummy.prop

    assert corbel_metadata(p) == {
        "json": {},
        "ignore": False,
        "allow_none": False,
        "validator": None,
        "serializer": None,
        "deserializer": None,
    }


def test_corbel_metadata_returns_nested_value():
    f = dataclasses.field(metadata={"corbel": {"json": {"key": "value"}}})
    assert corbel_metadata(f, "json.key") == "value"


def test_corbel_metadata_returns_default_for_missing_key():
    f = dataclasses.field(metadata={"corbel": {"json": {"key": "value"}}})
    assert corbel_metadata(f, "json.missing", default=42) == 42


def test_corbel_metadata_returns_default_for_non_dict_in_path():
    f = dataclasses.field(metadata={"corbel": {"json": "not_a_dict"}})
    assert corbel_metadata(f, "json.key", default=99) == 99


def test_corbel_metadata_returns_default_when_path_missing():
    f = dataclasses.field(metadata={"corbel": {"foo": {"bar": 1}}})
    assert corbel_metadata(f, "foo.baz", default="x") == "x"
