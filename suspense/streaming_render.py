import asyncio
import logging
from concurrent import futures

from django.template import loader

logger = logging.getLogger(__name__)


def streaming_render(request, template_name, context=None, using=None):
    context = context or {}
    context["is_async"] = False
    content, tasks = _render_base_template(context, request, template_name, using)
    yield content
    if tasks:
        with futures.ThreadPoolExecutor() as executor:
            tasks = [executor.submit(task) for task in tasks]
            for task in futures.as_completed(tasks):
                try:
                    uid, result = task.result()
                    yield _render_replacer(result, request, uid, using)
                except Exception:
                    logger.exception(
                        f'failed to render suspense template "{template_name}"'
                    )


async def async_streaming_render(request, template_name, context=None, using=None):
    context = context or {}
    context["is_async"] = True
    content, tasks = _render_base_template(context, request, template_name, using)
    yield content
    if tasks:
        for task in asyncio.as_completed([asyncio.create_task(task) for task in tasks]):
            try:
                uid, result = await task
                yield _render_replacer(result, request, uid, using)
            except asyncio.CancelledError:
                raise
            except Exception:
                logger.exception(
                    f'failed to render suspense template "{template_name}"'
                )


def _render_replacer(result, request, uid, using):
    escaped_string = result.replace('`', '\\`')
    return loader.render_to_string(
        "suspense/replacer.html",
        {
            "uid": uid,
            "escaped_string": escaped_string,
            "request": request,
        },
        request,
        using=using,
    )


def _render_base_template(context, request, template_name, using):
    content = loader.render_to_string(template_name, context, request, using=using)
    if hasattr(request, "_suspense"):
        tasks = request._suspense
        delattr(request, "_suspense")
    else:
        tasks = []
    return content, tasks
