import lxml.etree
import pytest

from main import extract


def test_basic():
    inp = "<baz><foo>bar</foo></baz>"
    mp = [{"column": "foo", "path": "foo"}]
    et = lxml.etree.fromstring(inp)
    assert extract(et, mp) == {"foo": "bar"}


def test_array():
    inp = "<baz><foo>bar</foo><foo>bar2</foo></baz>"
    mp = [{"column": "foo", "path": "foo", "array": True}]
    et = lxml.etree.fromstring(inp)
    assert extract(et, mp) == {"foo": ["bar", "bar2"]}

    with pytest.raises(ValueError):
        del mp[0]["array"]
        extract(et, mp)


def test_empty():
    inp = "<baz><foo>bar</foo></baz>"
    mp = [{"column": "bak", "path": "bak"}]
    et = lxml.etree.fromstring(inp)
    assert extract(et, mp) == {"bak": None}


def test_nested_and_array():
    inp = "<baz><foo><bak>a1</bak><bak>a2</bak></foo></baz>"
    mp = [
        {
            "column": "foo",
            "path": "foo",
            "mapping": [
                {"column": "bak", "path": "bak", "array": True},
            ],
        }
    ]
    et = lxml.etree.fromstring(inp)
    assert extract(et, mp) == {"foo": {"bak": ["a1", "a2"]}}


def test_attr_and_nested():
    inp = '<baz><foo prop="abc">bar</foo></baz>'
    mp = [
        {
            "column": "bak",
            "path": "foo",
            "mapping": [
                {"column": "nested", "path": None},
                {"column": "nested2", "path": "#prop"},
            ],
        }
    ]
    et = lxml.etree.fromstring(inp)
    assert extract(et, mp) == {"bak": {"nested": "bar", "nested2": "abc"}}


def test_atts():
    inp = '<baz><foo a="b" c="d">abc</foo></baz>'
    mp = [{"column": "foo", "path": "foo", "attrs": {"a": "b", "c": "d"}}]
    et = lxml.etree.fromstring(inp)
    assert extract(et, mp) == {"foo": "abc"}

    with pytest.raises(KeyError):
        mp[0]["attrs"] = {"b": "c"}
        et = lxml.etree.fromstring(inp)
        extract(et, mp)
