import pytest
from django.http import HttpRequest

from suspense.streaming_render import streaming_render


def test_suspense_template_response():
    def bar_loader():
        yield 'bar'

    streaming_content = streaming_render(
        HttpRequest(), "test_suspense.html", {"bar_loader": bar_loader}
    )
    assert 'foo' in next(streaming_content)
    assert 'bar' in next(streaming_content)
    with pytest.raises(StopIteration):
        next(streaming_content)


def test_suspense_exception(caplog):
    exception = Exception('bar')

    def bar_loader():
        raise exception

    streaming_content = streaming_render(
        HttpRequest(), "test_suspense.html", {"bar_loader": bar_loader}
    )
    assert 'foo' in next(streaming_content)
    with pytest.raises(StopIteration):
        next(streaming_content)

    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'ERROR'
    assert (
        caplog.records[0].message
        == 'failed to render suspense template "test_suspense.html"'
    )
    assert caplog.records[0].exc_info[1] == exception
