import pytest
from django.http import HttpRequest

from suspense.shortcuts import render


@pytest.mark.asyncio
async def test_render():
    request = HttpRequest()
    response = render(request, "test.html")
    streaming_content = response.streaming_content
    assert (await anext(streaming_content)) == b'foo\n'
    with pytest.raises(StopAsyncIteration):
        await anext(streaming_content)
