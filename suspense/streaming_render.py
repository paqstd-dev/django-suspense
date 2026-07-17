import asyncio
import logging
from concurrent import futures

from django.template import loader

logger = logging.getLogger(__name__)


def streaming_render(request, template_name, context=None, using=None):
    context = {**context} if context else {}
    context["_suspense_is_async"] = False
    content, tasks = _render_base_template(context, request, template_name, using)
    yield content
    if tasks:
        executor = futures.ThreadPoolExecutor()
        try:
            submitted = [executor.submit(task) for task in tasks]
            for future in futures.as_completed(submitted):
                try:
                    uid, result = future.result()
                    yield _render_replacer(result, request, uid, using)
                except Exception:
                    logger.exception(
                        f'failed to render suspense template "{template_name}"'
                    )
        finally:
            executor.shutdown(wait=False, cancel_futures=True)


async def async_streaming_render(request, template_name, context=None, using=None):
    context = {**context} if context else {}
    context["_suspense_is_async"] = True
    content, tasks = await asyncio.to_thread(
        _render_base_template, context, request, template_name, using
    )
    yield content
    if tasks:
        pending = [asyncio.ensure_future(task()) for task in tasks]
        try:
            for task in asyncio.as_completed(pending):
                try:
                    uid, result = await task
                    yield await asyncio.to_thread(
                        _render_replacer, result, request, uid, using
                    )
                except asyncio.CancelledError:
                    raise
                except Exception:
                    logger.exception(
                        f'failed to render suspense template "{template_name}"'
                    )
        finally:
            for task in pending:
                task.cancel()


def _render_replacer(result, request, uid, using):
    # escape JS template literal: \ ` ${
    escaped_string = (
        result.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')
    )
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
    tasks = getattr(request, "_suspense", [])
    for attr in ("_suspense", "_suspense_shared"):
        if hasattr(request, attr):
            delattr(request, attr)
    return content, tasks
