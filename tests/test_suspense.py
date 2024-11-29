from asyncio import iscoroutine

import pytest
from django import template
from django.http import HttpRequest


@pytest.mark.asyncio
async def test_suspense():
    mock_request = HttpRequest()
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
        .render(context={"request": mock_request})
    )

    assert 'abcdefg' not in html
    assert hasattr(mock_request, "_suspense")
    assert isinstance(mock_request._suspense, list)
    assert len(mock_request._suspense) == 1
    task = mock_request._suspense[0]
    assert iscoroutine(task)
    result = await task
    assert isinstance(result, tuple)
    assert isinstance(result[0], str)
    assert 'abcdefg' in result[1]


@pytest.mark.asyncio
async def test_fallback():
    mock_request = HttpRequest()
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
        .render(context={"request": mock_request})
    )

    assert 'abcdefg' not in html
    assert 'loading...' in html
    assert hasattr(mock_request, "_suspense")
    assert isinstance(mock_request._suspense, list)
    assert len(mock_request._suspense) == 1
    task = mock_request._suspense[0]
    assert iscoroutine(task)
    result = await task
    assert isinstance(result, tuple)
    assert isinstance(result[0], str)
    assert 'abcdefg' in result[1]
