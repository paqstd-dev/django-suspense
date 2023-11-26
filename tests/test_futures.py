from concurrent.futures import Future

from django import template

from suspense.futures import __futures, create, get


def test_create_future():
    nodelist = template.base.NodeList()
    context = template.context.Context()

    uid = create(nodelist, context)
    assert isinstance(__futures[uid], Future)


def test_get_future():
    nodelist = template.engines['django'].from_string(
        "{% for x in y %}{{x}}{% endfor %}"
    )
    context = {'y': 'abc'}

    uid = create(nodelist, context)
    assert get(uid) == 'abc'


def test_get_None_key():
    assert get('incorrect-key') is None
