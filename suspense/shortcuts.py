from .http import AsyncSuspenseTemplateResponse, SuspenseTemplateResponse


def render(
    request, template_name, context=None, content_type=None, status=None, using=None
):
    return SuspenseTemplateResponse(
        request,
        template_name,
        context,
        using=using,
        content_type=content_type,
        status=status,
    )


def async_render(
    request, template_name, context=None, content_type=None, status=None, using=None
):
    return AsyncSuspenseTemplateResponse(
        request,
        template_name,
        context,
        using=using,
        content_type=content_type,
        status=status,
    )
