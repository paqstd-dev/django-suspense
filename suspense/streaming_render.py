import logging
from concurrent import futures

from django.template import loader

logger = logging.getLogger(__name__)


def streaming_render(request, template_name, context=None, using=None):
    content = loader.render_to_string(template_name, context, request, using=using)
    if hasattr(request, "_suspense"):
        tasks = request._suspense
        delattr(request, "_suspense")
    else:
        tasks = []
    yield content
    if tasks:
        with futures.ThreadPoolExecutor() as executor:
            tasks = [executor.submit(task) for task in tasks]
            for task in futures.as_completed(tasks):
                try:
                    uid, result = task.result()
                    escaped_string = result.replace('`', '\\`')
                    yield loader.render_to_string(
                        "suspense/replacer.html",
                        {
                            "uid": uid,
                            "escaped_string": escaped_string,
                            "request": request,
                        },
                        request,
                        using=using,
                    )
                except Exception:
                    logger.exception(
                        f'failed to render suspense template "{template_name}"'
                    )
