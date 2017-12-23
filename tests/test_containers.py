# coding: utf-8

import pytest

from jzqt.containers import ObjectDict


class TestObjectDict(object):

    def test_init(self):
        assert ObjectDict() == dict()
        assert ObjectDict({'a': 'b'}) == {'a': 'b'}
        assert ObjectDict(a=1, b=2) == dict(a=1, b=2)
        iterable_object = [('a', 1), (2, None), (None, ''), ('', False)]
        assert ObjectDict(iterable_object) == dict(iterable_object)

    def test_get_attr(self):
        obj = ObjectDict({
            'name': 'JZQT',
            'get': 'data'
        })
        assert obj.name == 'JZQT'
        assert obj.get != 'data'
        assert obj['get'] == 'data'

    def test_getattr_raise_attribute_error(self):
        obj = ObjectDict()
        with pytest.raises(AttributeError) as exc_info:
            print(obj.not_exist_attr)
        assert exc_info.value.args == ('not_exist_attr',)

    def test_set_attr(self):
        obj = ObjectDict()
        obj.name = 'JZQT'
        obj.get = 1
        assert obj['name'] == 'JZQT'
        assert obj['get'] == 1
