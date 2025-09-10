import dataclasses

from corbel._utils._capture_obj import capture_obj


@dataclasses.dataclass
class Dummy:
    x: int
    y: str


def test_capture_obj_with_dataclass():
    stack = []
    obj = Dummy(1, "a")
    result = capture_obj(None, obj, stack)
    assert isinstance(result, dict)
    assert result["x"] == 1
    assert result["y"] == "a"


def test_capture_obj_with_list_and_stack():
    stack = []
    lst = [1, 2]
    result = capture_obj(None, lst, stack)
    assert result == []
    assert len(stack) == 2
    assert stack[0][1] in lst


def test_capture_obj_with_tuple_and_stack():
    stack = []
    tpl = (3, 4)
    result = capture_obj(None, tpl, stack)
    assert result == []
    assert len(stack) == 2
    values = [entry[1] for entry in stack]
    assert 3 in values and 4 in values


def test_capture_obj_with_dict_and_stack():
    stack = []
    d = {"a": 1, "b": 2}
    result = capture_obj(None, d, stack)
    assert result == {}
    assert len(stack) == 2
    keys = [entry[3] for entry in stack]
    assert "a" in keys and "b" in keys


def test_capture_obj_with_regular_value():
    stack = []
    val = 42
    result = capture_obj(None, val, stack)
    assert result == 42
    assert stack == []
