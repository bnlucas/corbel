import dataclasses

from corbel._utils._field import field


def test_field_basic_metadata():
    f = field()
    assert isinstance(f, dataclasses.Field)
    assert "corbel" in f.metadata
    assert f.metadata["corbel"]["json"] == {}
    assert f.metadata["corbel"]["allow_none"] is False
    assert f.metadata["corbel"]["validator"] is None


def test_field_with_custom_metadata():
    custom_meta = {"foo": "bar"}
    f = field(metadata=custom_meta)
    assert f.metadata["foo"] == "bar"
    assert "corbel" in f.metadata
    assert f.metadata["corbel"]["json"] == {}
    assert f.metadata["corbel"]["allow_none"] is False
    assert f.metadata["corbel"]["validator"] is None


def test_field_with_json_and_validator():
    def validator(x):
        return x > 0

    f = field(json={"key": "value"}, validator=validator, allow_none=True)
    corbel_meta = f.metadata["corbel"]
    assert corbel_meta["json"] == {"key": "value"}
    assert corbel_meta["validator"] is validator
    assert corbel_meta["allow_none"] is True


def test_field_with_default_and_default_factory():
    f1 = field(default=10)
    assert f1.default == 10
    assert (
        not hasattr(f1, "default_factory") or f1.default_factory is dataclasses.MISSING
    )
    f2 = field(default_factory=list)
    assert callable(f2.default_factory)
    assert not hasattr(f2, "default") or f2.default is dataclasses.MISSING


def test_field_passes_standard_args():
    f = field(init=False, repr=False, compare=False, hash=True)
    assert f.init is False
    assert f.repr is False
    assert f.compare is False
    assert f.hash is True


def test_field_merges_corbel_dict():
    f = field(corbel={"extra": 123})
    corbel_meta = f.metadata["corbel"]
    assert corbel_meta["extra"] == 123
    assert corbel_meta["json"] == {}
    assert corbel_meta["allow_none"] is False
    assert corbel_meta["validator"] is None
