import dataclasses

from corbel._utils._capture_member import capture_member


@dataclasses.dataclass
class Dummy:
    x: int
    y: str


def test_capture_member_with_regular_value():
    val = 42
    result = capture_member(None, val)
    assert result == 42


def test_capture_member_with_dataclass():
    obj = Dummy(1, "a")
    result = capture_member(None, obj)
    assert isinstance(result, dict)
    assert result["x"] == 1
    assert result["y"] == "a"


def test_capture_member_with_list():
    lst = [1, 2]
    result = capture_member(None, lst)
    assert result == [1, 2]


def test_capture_member_with_nested_list_and_dict():
    data = [{"a": 1}, {"b": 2}]
    result = capture_member(None, data)
    assert result == [{"a": 1}, {"b": 2}]


def test_capture_member_with_custom_capture_fn():
    called = []

    def fake_capture(member, value, stack, **kwargs):
        called.append((member, value))
        return f"captured-{value}"

    result = capture_member(None, [1, 2], capture_fn=fake_capture)
    assert result == "captured-[1, 2]"
    assert len(called) == 1
