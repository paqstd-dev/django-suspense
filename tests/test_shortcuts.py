import pytest
from django.http import HttpRequest

from suspense.shortcuts import render


def test_render():
    request = HttpRequest()
    response = render(request, "test.html")
    streaming_content = response.streaming_content
    assert next(streaming_content) == b'foo\n'
    with pytest.raises(StopIteration):
        next(streaming_content)
