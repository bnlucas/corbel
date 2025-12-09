from dataclasses import dataclass

import pytest

from corbel import Serializable, field
from corbel._utils._from_json import from_json


@dataclass
class Dummy(Serializable):
    x: int = field()


def test_from_json_with_wrapper():
    obj = from_json(Dummy, '{"wrapper": {"x": 5}}', wrapper="wrapper")

    assert obj.x == 5


def test_from_json_rejects_unknown_kwargs():
    with pytest.raises(TypeError):
        from_json(Dummy, '{"x": 1}', object_pairs_hook=dict)


def test_from_json_passes_hooks():
    seen = {}

    def hook(obj):
        seen.update(obj)
        return obj

    obj = from_json(Dummy, '{"x": 2}', object_hook=hook)

    assert obj.x == 2
    assert seen == {"x": 2}
