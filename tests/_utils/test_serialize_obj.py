import dataclasses
from datetime import datetime, date, time
from enum import Enum
from uuid import UUID

from corbel._utils._serialize_obj import serialize_obj


@dataclasses.dataclass
class Dummy:
    x: int
    y: str


class DummyEnum(Enum):
    A = "a"
    B = "b"


def test_serialize_obj_with_regular_value():
    stack = []
    val = 123
    assert serialize_obj(None, val, stack) == 123
    assert stack == []


def test_serialize_obj_with_dataclass():
    stack = []
    obj = Dummy(1, "test")
    result = serialize_obj(None, obj, stack)
    assert isinstance(result, dict)
    assert result["x"] == 1
    assert result["y"] == "test"


def test_serialize_obj_with_list_and_stack():
    stack = []
    lst = [1, 2]
    items = serialize_obj(None, lst, stack)
    assert items == []
    assert len(stack) == 2
    assert stack[0][1] in lst


def test_serialize_obj_with_dict_and_stack():
    stack = []
    d = {"a": 1, "b": 2}
    result = serialize_obj(None, d, stack)
    assert result == {}
    assert len(stack) == 2
    keys = [entry[3] for entry in stack]
    assert "a" in keys and "b" in keys


def test_serialize_obj_with_enum():
    stack = []
    e = DummyEnum.A
    assert serialize_obj(None, e, stack) == "a"
    assert stack == []


def test_serialize_obj_with_datetime_types():
    stack = []
    dt = datetime(2025, 1, 1, 12, 0)
    d = date(2025, 1, 1)
    t = time(12, 0)
    assert serialize_obj(None, dt, stack) == dt.isoformat()
    assert serialize_obj(None, d, stack) == d.isoformat()
    assert serialize_obj(None, t, stack) == t.isoformat()


def test_serialize_obj_with_uuid():
    stack = []
    u = UUID("12345678-1234-5678-1234-567812345678")
    assert serialize_obj(None, u, stack) == str(u)
