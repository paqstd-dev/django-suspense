from django import template

from suspense.futures import create


def test_create_future():
    nodelist = template.base.NodeList()
    context = template.context.Context()

    uid, task = create(nodelist, context)
    result = task()
    assert isinstance(result, tuple)
    assert result[0] == uid
    assert result[1] == ''
