import dataclasses
from datetime import date, datetime, time
from enum import Enum
from typing import Dict
from uuid import UUID

import pytest

from corbel._utils._deserialize_value import deserialize_value


class DummyEnum(Enum):
    A = 1
    B = 2


@dataclasses.dataclass
class DummyDataclass:
    a: int
    b: str


def test_basic_types():
    assert deserialize_value(5, int) == 5
    assert deserialize_value("x", str) == "x"
    assert deserialize_value(3.14, float) == 3.14
    assert deserialize_value(True, bool) is True


def test_optional_types():
    assert deserialize_value(None, int | None) is None
    assert deserialize_value(10, int | None) == 10
    with pytest.raises(TypeError):
        deserialize_value(None, int)


def test_list_and_tuple():
    assert deserialize_value([1, 2], list[int]) == [1, 2]
    assert deserialize_value([1, 2], tuple[int, int]) == (1, 2)


def test_dict():
    val = {"x": 1, "y": 2}
    res = deserialize_value(val, Dict[str, int])
    assert res == val


def test_enum():
    assert deserialize_value(1, DummyEnum) is DummyEnum.A
    assert deserialize_value(2, DummyEnum) is DummyEnum.B


def test_datetime_types():
    dt = datetime.now().isoformat()
    d = date.today().isoformat()
    t = time(12, 0).isoformat()
    assert deserialize_value(dt, datetime).isoformat() == dt
    assert deserialize_value(d, date).isoformat() == d
    assert deserialize_value(t, time).isoformat() == t


def test_uuid():
    u = UUID("12345678-1234-5678-1234-567812345678")
    assert str(deserialize_value(str(u), UUID)) == str(u)


def test_dataclass():
    data = {"a": 1, "b": "x"}
    obj = deserialize_value(data, DummyDataclass)
    assert isinstance(obj, DummyDataclass)
    assert obj.a == 1
    assert obj.b == "x"


def test_union_failure():
    from typing import Union

    with pytest.raises(TypeError):
        deserialize_value("x", Union[int, float])
