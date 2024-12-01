from .http import SuspenseTemplateResponse


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
