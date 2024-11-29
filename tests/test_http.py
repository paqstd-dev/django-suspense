import pytest

from suspense.http import SuspenseTemplateResponse


@pytest.mark.asyncio
async def test_suspense_template_response():
    response = SuspenseTemplateResponse(None, "test.html")
    streaming_content = response.streaming_content
    assert (await anext(streaming_content)) == b'foo\n'
    with pytest.raises(StopAsyncIteration):
        await anext(streaming_content)
