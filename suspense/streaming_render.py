import asyncio
import logging

from django.template import loader

logger = logging.getLogger(__name__)


def get_html(uid, escaped_string):
    return f"""<script>
        document.getElementById("suspense-loader-{uid}").innerHTML = `{escaped_string}`;
    </script>
    """


async def streaming_render(request, template_name, context=None, using=None):
    content = loader.render_to_string(template_name, context, request, using=using)
    if hasattr(request, "_suspense"):
        tasks = request._suspense
        delattr(request, "_suspense")
    else:
        tasks = []
    yield content
    if tasks:
        for task in asyncio.as_completed(tasks):
            try:
                uid, result = await task
                escaped_string = result.replace('`', '\\`')
                yield get_html(uid, escaped_string)
            except asyncio.CancelledError:
                pass
            except Exception:
                logger.exception(f'failed to render suspense template {template_name}"')
