import asyncio

import pytest
from django import template
from django.template import Template

from suspense.futures import create, create_async


def test_create_future():
    t = Template("<div>{{ a }}</div>")
    context = template.context.Context()
    context.push({'a': 'bar'})
    uid, task = create(t.nodelist, context)
    result = task()
    assert isinstance(result, tuple)
    assert result[0] == uid
    assert result[1] == "<div>bar</div>"


@pytest.mark.asyncio
async def test_create_async_future_without_context_keys():
    t = Template("<div>{{ a }}</div>")
    nodelist = t.nodelist
    context = template.context.Context()

    async def a():
        return 'bar'

    context.push({'a': asyncio.create_task(a())})

    uid, task = create_async(nodelist, context, ['a'])
    result = await task
    assert isinstance(result, tuple)
    assert result[0] == uid
    assert result[1] == '<div>bar</div>'


@pytest.mark.asyncio
async def test_create_async_future_with_context_keys():
    t = Template("<div>{{ a }}</div>")
    nodelist = t.nodelist
    context = template.context.Context()

    async def a():
        return 'bar'

    context.push({'a': asyncio.create_task(a())})

    uid, task = create_async(nodelist, context, [])
    result = await task
    assert isinstance(result, tuple)
    assert result[0] == uid
    assert result[1] == '<div>bar</div>'
