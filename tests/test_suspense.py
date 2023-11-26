from django import template


def test_suspense():
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
        .render()
    )

    assert 'abcdefg' not in html


def test_fallback():
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
        .render()
    )

    assert 'abcdefg' not in html
    assert 'loading...' in html
