from django.test.client import RequestFactory

from suspense.http import SuspenseTemplateResponse
from suspense.views import SuspenseTemplateView


def test_suspense_template_response():
    request = RequestFactory().get('/')
    response = SuspenseTemplateView.as_view(template_name="test_suspense.html")(request)
    assert isinstance(response, SuspenseTemplateResponse)
