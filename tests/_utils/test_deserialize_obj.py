import dataclasses
from datetime import datetime, date, time
from enum import Enum
from uuid import UUID

from corbel._utils._deserialize_obj import deserialize_obj


@dataclasses.dataclass
class Dummy:
    x: int


def dummy_deserialize_fn(value, typ):
    return value


class Color(Enum):
    RED = "red"
    BLUE = "blue"


def test_deserialize_obj_dataclass():
    value = {"x": 5}
    result = deserialize_obj(value, Dummy, None, dummy_deserialize_fn)
    assert isinstance(result, Dummy)
    assert result.x == 5


def test_deserialize_obj_list():
    value = [1, 2, 3]
    result = deserialize_obj(value, list[int], list, dummy_deserialize_fn)
    assert result == [1, 2, 3]


def test_deserialize_obj_tuple():
    value = [1, 2]
    result = deserialize_obj(value, tuple[int, int], tuple, dummy_deserialize_fn)
    assert result == (1, 2)


def test_deserialize_obj_dict():
    value = {"a": 1, "b": 2}
    result = deserialize_obj(value, dict[str, int], dict, dummy_deserialize_fn)
    assert result == {"a": 1, "b": 2}


def test_deserialize_obj_enum():
    result = deserialize_obj("red", Color, None, dummy_deserialize_fn)
    assert result is Color.RED


def test_deserialize_obj_datetime():
    dt_str = "2025-09-09T12:34:56"
    result = deserialize_obj(dt_str, datetime, None, dummy_deserialize_fn)
    assert isinstance(result, datetime)
    assert result.isoformat() == dt_str


def test_deserialize_obj_date():
    d_str = "2025-09-09"
    result = deserialize_obj(d_str, date, None, dummy_deserialize_fn)
    assert isinstance(result, date)
    assert result.isoformat() == d_str


def test_deserialize_obj_time():
    t_str = "12:34:56"
    result = deserialize_obj(t_str, time, None, dummy_deserialize_fn)
    assert isinstance(result, time)
    assert result.isoformat() == t_str


def test_deserialize_obj_uuid():
    u_str = "12345678-1234-5678-1234-567812345678"
    result = deserialize_obj(u_str, UUID, None, dummy_deserialize_fn)
    assert isinstance(result, UUID)
    assert str(result) == u_str


def test_deserialize_obj_fallback():
    val = 42
    result = deserialize_obj(val, int, None, dummy_deserialize_fn)
    assert result == 42
