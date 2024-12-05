from django.views.generic import TemplateView

from suspense.http import AsyncSuspenseTemplateResponse, SuspenseTemplateResponse


class SuspenseTemplateView(TemplateView):
    response_class = SuspenseTemplateResponse


class AsyncSuspenseTemplateView(TemplateView):
    response_class = AsyncSuspenseTemplateResponse

    async def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
