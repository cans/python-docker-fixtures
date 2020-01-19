# -*- coding: utf-8; -*-
import pytest

from dockerfixtures.container import _prune_dict


@pytest.mark.parametrize('dictionary', [{'a': {'b': None}}, {'a': {'b': {'c': {}}}}, {}])
def test__prune_dict_with_empty_nested_dicts(dictionary):
    # When
    res = _prune_dict(dictionary)
    # Then
    assert res == {}


@pytest.mark.parametrize('dictionary', [{'a': {'b': None}, 'k': 1},
                                        {'a': {'b': {'c': {}}}, 'k': 1},
                                        {'k': 1}])
def test__prune_dict_with_non_empty_dict_but_empty_nested_dicts(dictionary):
    # When
    res = _prune_dict(dictionary)
    # Then
    assert res == {'k': 1}


@pytest.mark.parametrize('dictionary,expected',
                         [({'a': {'b': None, 'k': 1}, 'l': None}, {'a': {'k': 1}}),
                          ({'a': {'b': {'c': {}, 'k': 1}, 'l': None}, 'm': None},
                           {'a': {'b': {'k': 1}}}),
                          ({'k': 1, 'l': None}, {'k': 1}),
                          ])
def test__prune_dict_with_non_empty_nested_dicts(dictionary, expected):
    # When
    res = _prune_dict(dictionary)
    # Then
    assert res == expected


# vim: et:sw=4:syntax=python:ts=4:
