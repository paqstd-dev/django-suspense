import pytest
from django.http import HttpRequest

from suspense.http import AsyncSuspenseTemplateResponse, SuspenseTemplateResponse


def test_suspense_template_response():
    response = SuspenseTemplateResponse(HttpRequest(), "test.html")
    streaming_content = response.streaming_content
    assert next(streaming_content) == b'foo\n'
    with pytest.raises(StopIteration):
        next(streaming_content)


@pytest.mark.asyncio
async def test_async_suspense_template_response():
    response = AsyncSuspenseTemplateResponse(HttpRequest(), "test.html")
    streaming_content = response.streaming_content
    assert await streaming_content.__anext__() == b'foo\n'
    with pytest.raises(StopAsyncIteration):
        await streaming_content.__anext__()
