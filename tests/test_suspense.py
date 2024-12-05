import pytest
from django import template
from django.http import HttpRequest


def test_suspense():
    request = HttpRequest()
    html = (
        template.engines['django']
        .from_string(
            """
        {% load suspense %}

        {% suspense %}
            abcdefg
        {% endsuspense %}
    """
        )
        .render(context={"request": request, "is_async": False})
    )

    assert 'abcdefg' not in html
    assert hasattr(request, "_suspense")
    assert isinstance(request._suspense, list)
    assert len(request._suspense) == 1
    task = request._suspense[0]
    result = task()
    assert isinstance(result, tuple)
    assert isinstance(result[0], str)
    assert 'abcdefg' in result[1]


@pytest.mark.asyncio
async def test_suspense_async():
    request = HttpRequest()
    html = (
        template.engines['django']
        .from_string(
            """
        {% load suspense %}

        {% suspense %}
            abcdefg
        {% endsuspense %}
    """
        )
        .render(context={"request": request, "is_async": True})
    )

    assert 'abcdefg' not in html
    assert hasattr(request, "_suspense")
    assert isinstance(request._suspense, list)
    assert len(request._suspense) == 1
    task = request._suspense[0]
    result = await task
    assert isinstance(result, tuple)
    assert isinstance(result[0], str)
    assert 'abcdefg' in result[1]


def test_fallback():
    request = HttpRequest()
    html = (
        template.engines['django']
        .from_string(
            """
        {% load suspense %}

        {% suspense %}
            {% fallback %}
                loading...
            {% endfallback %}
            abcdefg
        {% endsuspense %}
    """
        )
        .render(context={"request": request, "is_async": False})
    )

    assert 'abcdefg' not in html
    assert 'loading...' in html
    assert hasattr(request, "_suspense")
    assert isinstance(request._suspense, list)
    assert len(request._suspense) == 1
    task = request._suspense[0]
    result = task()
    assert isinstance(result, tuple)
    assert isinstance(result[0], str)
    assert 'abcdefg' in result[1]


@pytest.mark.asyncio
async def test_fallback_async():
    request = HttpRequest()
    html = (
        template.engines['django']
        .from_string(
            """
        {% load suspense %}

        {% suspense %}
            {% fallback %}
                loading...
            {% endfallback %}
            abcdefg
        {% endsuspense %}
    """
        )
        .render(context={"request": request, "is_async": True})
    )

    assert 'abcdefg' not in html
    assert 'loading...' in html
    assert hasattr(request, "_suspense")
    assert isinstance(request._suspense, list)
    assert len(request._suspense) == 1
    task = request._suspense[0]
    result = await task
    assert isinstance(result, tuple)
    assert isinstance(result[0], str)
    assert 'abcdefg' in result[1]


def test_webkit_extra_invisible_bytes_not_webkit():
    request = HttpRequest()
    html = (
        template.engines['django']
        .from_string(
            """
        {% load suspense %}

        {% webkit_extra_invisible_bytes 10 %}
    """
        )
        .render(context={"request": request})
    )

    assert 'div' not in html


def test_webkit_extra_invisible_bytes_webkit():
    request = HttpRequest()
    request.META['HTTP_USER_AGENT'] = '... AppleWebKit/605.1.15 ...'
    html = (
        template.engines['django']
        .from_string(
            """
        {% load suspense %}

        {% webkit_extra_invisible_bytes 2 %}
    """
        )
        .render(context={"request": request})
    )

    assert '<div style="width: 0;height:0">\u200b\u200b</div>' not in html
