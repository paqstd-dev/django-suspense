import pytest
from django.test.client import RequestFactory

from suspense.http import AsyncSuspenseTemplateResponse, SuspenseTemplateResponse
from suspense.views import AsyncSuspenseTemplateView, SuspenseTemplateView


def test_suspense_template_response():
    request = RequestFactory().get('/')
    response = SuspenseTemplateView.as_view(template_name="test_suspense.html")(request)
    assert isinstance(response, SuspenseTemplateResponse)


@pytest.mark.asyncio
async def test_async_suspense_template_response():
    request = RequestFactory().get('/')
    response = await AsyncSuspenseTemplateView.as_view(
        template_name="test_suspense.html"
    )(request)
    assert isinstance(response, AsyncSuspenseTemplateResponse)
