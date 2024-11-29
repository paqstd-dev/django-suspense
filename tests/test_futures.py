from inspect import iscoroutine

import pytest
from django import template

from suspense.futures import create


@pytest.mark.asyncio
async def test_create_future():
    nodelist = template.base.NodeList()
    context = template.context.Context()

    uid, task = create(nodelist, context)
    assert iscoroutine(task)
    result = await task
    assert isinstance(result, tuple)
    assert result[0] == uid
    assert result[1] == ''
