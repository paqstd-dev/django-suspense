import pytest
from django.http import HttpRequest

from suspense.shortcuts import async_render, render


def test_render():
    request = HttpRequest()
    response = render(request, "test.html")
    streaming_content = response.streaming_content
    assert next(streaming_content) == b'foo\n'
    with pytest.raises(StopIteration):
        next(streaming_content)


@pytest.mark.asyncio
async def test_async_render():
    request = HttpRequest()
    response = async_render(request, "test.html")
    streaming_content = response.streaming_content
    assert await streaming_content.__anext__() == b'foo\n'
    with pytest.raises(StopAsyncIteration):
        await streaming_content.__anext__()
