from __future__ import annotations

from corbel._objects import CorbelProperty


class TestCorbelProperty:
    def test_metadata_stored(self):
        meta = {"ignore": True}

        class Foo:
            value = CorbelProperty(lambda self: 42)

        prop = Foo.__dict__["value"]

        assert prop.__corbel__["ignore"] is False

        prop_with_meta = CorbelProperty(lambda self: 1, **meta)

        assert "ignore" in prop_with_meta.__corbel__
        assert prop_with_meta.__corbel__["ignore"] is True

    def test_setter_preserves_metadata(self):
        meta = {"ignore": True}

        class Foo:
            value = CorbelProperty(lambda self: 42, **meta)

        def setter(self, v):
            pass

        prop = Foo.__dict__["value"].setter(setter)

        assert "ignore" in prop.__corbel__
        assert prop.__corbel__["ignore"] is True

    def test_deleter_preserves_metadata(self):
        meta = {"ignore": True}

        class Foo:
            value = CorbelProperty(lambda self: 42, **meta)

        def deleter(self):
            pass

        prop = Foo.__dict__["value"].deleter(deleter)
        assert "ignore" in prop.__corbel__
        assert prop.__corbel__["ignore"] is True

    def test_works_as_property(self):
        class Foo:
            def __init__(self):
                self._val = 0

            value = CorbelProperty(lambda self: self._val)

        f = Foo()
        fval_prop = Foo.__dict__["value"].setter(
            lambda self, v: setattr(self, "_val", v)
        )
        f.__class__.value = fval_prop

        f.value = 123

        assert f._val == 123
        assert f.value == 123
