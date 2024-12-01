from django.views.generic import TemplateView

from suspense.http import SuspenseTemplateResponse


class SuspenseTemplateView(TemplateView):
    response_class = SuspenseTemplateResponse
