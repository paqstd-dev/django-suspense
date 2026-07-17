import asyncio

import pytest
from django.http import HttpRequest

from suspense.streaming_render import (
    _render_replacer,
    async_streaming_render,
    streaming_render,
)


def test_streaming_render():
    def bar_loader():
        yield 'bar'

    streaming_content = streaming_render(
        HttpRequest(), "test_suspense.html", {"bar_loader": bar_loader}
    )
    assert 'foo' in next(streaming_content)
    assert 'bar' in next(streaming_content)
    with pytest.raises(StopIteration):
        next(streaming_content)


def test_streaming_render_exception(caplog):
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


@pytest.mark.asyncio
async def test_async_streaming_render():
    async def bar_loader():
        return 'bar'

    streaming_content = async_streaming_render(
        HttpRequest(), "test_suspense.html", {"bar_loader": bar_loader()}
    )
    assert 'foo' in await streaming_content.__anext__()
    assert 'bar' in await streaming_content.__anext__()
    with pytest.raises(StopAsyncIteration):
        await streaming_content.__anext__()


@pytest.mark.asyncio
async def test_async_streaming_render_exception(caplog):
    exception = Exception('bar')

    async def bar_loader():
        raise exception

    streaming_content = async_streaming_render(
        HttpRequest(), "test_suspense.html", {"bar_loader": bar_loader()}
    )
    assert 'foo' in await streaming_content.__anext__()
    with pytest.raises(StopAsyncIteration):
        await streaming_content.__anext__()

    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'ERROR'
    assert (
        caplog.records[0].message
        == 'failed to render suspense template "test_suspense.html"'
    )
    assert caplog.records[0].exc_info[1] == exception


@pytest.mark.asyncio
async def test_async_streaming_render_cancel(caplog):
    exception = Exception('bar')

    async def bar_loader():
        raise exception

    task = asyncio.create_task(bar_loader())
    streaming_content = async_streaming_render(
        HttpRequest(), "test_suspense.html", {"bar_loader": task}
    )

    task.cancel()
    assert 'foo' in await streaming_content.__anext__()
    with pytest.raises(asyncio.CancelledError):
        await streaming_content.__anext__()

    assert len(caplog.records) == 0


@pytest.mark.asyncio
async def test_async_streaming_render_shared_coroutine():
    async def shared_loader():
        return 'bar'

    streaming_content = async_streaming_render(
        HttpRequest(), "test_suspense_shared.html", {"shared": shared_loader()}
    )

    first = await streaming_content.__anext__()
    assert 'first-fallback' in first
    assert 'second-fallback' in first

    chunks = [await streaming_content.__anext__(), await streaming_content.__anext__()]
    assert any('first-bar' in chunk for chunk in chunks)
    assert any('second-bar' in chunk for chunk in chunks)
    with pytest.raises(StopAsyncIteration):
        await streaming_content.__anext__()


def test_render_replacer_escapes_js_template_literal():
    html = _render_replacer('a`b\\c${d}', HttpRequest(), 'uid123', None)
    assert 'a\\`b\\\\c\\${d}' in html
