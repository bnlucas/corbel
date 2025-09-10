from corbel.enums import Include


def test_include_enum():
    assert Include.ALWAYS.name == "ALWAYS"
    assert Include.NON_NONE.name == "NON_NONE"
    assert Include.NON_EMPTY.name == "NON_EMPTY"
    assert Include.NON_DEFAULT.name == "NON_DEFAULT"
