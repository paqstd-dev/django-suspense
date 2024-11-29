from django.views.generic import TemplateView

from suspense.http import SuspenseTemplateResponse


class SuspenseTemplateView(TemplateView):
    response_class = SuspenseTemplateResponse

    async def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
