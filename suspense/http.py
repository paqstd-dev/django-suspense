from django.http import StreamingHttpResponse

from .streaming_render import async_streaming_render, streaming_render


class SuspenseTemplateResponse(StreamingHttpResponse):
    def __init__(
        self,
        request,
        template,
        context=None,
        using=None,
        status=None,
        content_type=None,
    ):
        super().__init__(
            streaming_render(request, template, context, using=using),
            content_type=content_type,
            status=status,
        )


class AsyncSuspenseTemplateResponse(StreamingHttpResponse):
    def __init__(
        self,
        request,
        template,
        context=None,
        using=None,
        status=None,
        content_type=None,
    ):
        super().__init__(
            async_streaming_render(request, template, context, using=using),
            content_type=content_type,
            status=status,
        )
