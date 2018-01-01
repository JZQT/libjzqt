# coding: utf-8

import pytest

from jzqt.importools import import_object


@pytest.mark.parametrize('name, obj', [
    ('pytest', pytest),
    ('pytest.raises', pytest.raises),
    ('pytest.collect', pytest.collect),
    ('jzqt.importools.import_object', import_object),
])
def test_import_object(name, obj):
    assert import_object(name) is obj


@pytest.mark.parametrize('name, msg', [
    ('not_exist_module', None),
    ('time.not_exist_object', 'cannot from time import not_exist_object'),
    ('os.not_exist_module.not_exist_object', None),
])
def test_import_object_raise_error(name, msg):
    with pytest.raises(ImportError) as exc_info:
        import_object(name)
    if msg is not None:
        assert exc_info.value.args == (msg,)
