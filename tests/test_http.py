import pytest
from django.http import HttpRequest

from suspense.http import SuspenseTemplateResponse


def test_suspense_template_response():
    response = SuspenseTemplateResponse(HttpRequest(), "test.html")
    streaming_content = response.streaming_content
    assert next(streaming_content) == b'foo\n'
    with pytest.raises(StopIteration):
        next(streaming_content)
