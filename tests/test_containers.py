# coding: utf-8

import pytest

from jzqt.containers import ObjectDict, FrozenDict


class TestObjectDict(object):

    def test_init(self):
        assert ObjectDict() == dict()
        assert ObjectDict({'a': 'b'}) == {'a': 'b'}
        assert ObjectDict(a=1, b=2) == dict(a=1, b=2)
        iterable_object = [('a', 1), (2, None), (None, ''), ('', False)]
        assert ObjectDict(iterable_object) == dict(iterable_object)

    def test_getattr(self):
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

    def test_setattr(self):
        obj = ObjectDict()
        obj.name = 'JZQT'
        obj.get = 1
        assert obj['name'] == 'JZQT'
        assert obj['get'] == 1

    def test_delattr(self):
        obj = ObjectDict({'name': 'jzqt'})
        del obj.name
        assert obj == ObjectDict()

    def test_delattr_raise_attribute_error(self):
        obj = ObjectDict()
        with pytest.raises(AttributeError) as exc_info:
            del obj.name
        assert exc_info.value.args == ('name',)


class TestFrozenDict(object):

    _frozendict_samples = [
        FrozenDict(),
        FrozenDict({'key': 'value'}),
        FrozenDict({'key': False}),
        FrozenDict({'key': None}),
        FrozenDict({'key': True}),
        FrozenDict({'key': FrozenDict({'foo': 'bar', 'key': 1})}),
    ]

    @pytest.mark.parametrize('frozendict', _frozendict_samples)
    def test_str(self, frozendict):
        assert str(frozendict) == 'FrozenDict({})'.format(dict(frozendict))

    @pytest.mark.parametrize('frozendict', _frozendict_samples)
    def test_repr(self, frozendict):
        assert repr(frozendict) == 'FrozenDict({})'.format(dict(frozendict))

    def test_setitem(self):
        with pytest.raises(NotImplementedError) as exc_info:
            FrozenDict()['key'] = 'value'
        assert exc_info.value.args == ('FrozenDict.__setitem__',)

        with pytest.raises(NotImplementedError) as exc_info:
            FrozenDict().__setitem__('key', 'value')
        assert exc_info.value.args == ('FrozenDict.__setitem__',)

    def test_delitem(self):
        with pytest.raises(NotImplementedError) as exc_info:
            del FrozenDict()['key']
        assert exc_info.value.args == ('FrozenDict.__delitem__',)

        with pytest.raises(NotImplementedError) as exc_info:
            FrozenDict().__delitem__('key')
        assert exc_info.value.args == ('FrozenDict.__delitem__',)

    def test_clear(self):
        with pytest.raises(NotImplementedError) as exc_info:
            FrozenDict().clear()
        assert exc_info.value.args == ('FrozenDict.clear',)

    def test_update(self):
        with pytest.raises(NotImplementedError) as exc_info:
            FrozenDict().update({})
        assert exc_info.value.args == ('FrozenDict.update',)

    def test_pop(self):
        with pytest.raises(NotImplementedError) as exc_info:
            FrozenDict().pop('key')
        assert exc_info.value.args == ('FrozenDict.pop',)

    def test_popitem(self):
        with pytest.raises(NotImplementedError) as exc_info:
            FrozenDict().popitem()
        assert exc_info.value.args == ('FrozenDict.popitem',)

    def test_setdefault(self):
        with pytest.raises(NotImplementedError) as exc_info:
            FrozenDict().setdefault('key', 'value')
        assert exc_info.value.args == ('FrozenDict.setdefault',)

    def test_copy(self):
        x = FrozenDict({'a': {}})
        assert isinstance(x.copy(), FrozenDict)
        assert x['a'] is x.copy()['a']

    def test_fromkeys(self):
        res = FrozenDict.fromkeys(['a'])
        assert isinstance(res, FrozenDict)
        assert res == FrozenDict({'a': None})
