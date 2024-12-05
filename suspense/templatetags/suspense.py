from copy import copy

from django import template
from django.utils.safestring import mark_safe

from suspense.futures import create, create_async

register = template.Library()


@register.tag(name="suspense")
def suspense_tag(parser, token):
    nodelist = parser.parse(("endsuspense",))

    async_context_keys = token.split_contents()[1:]
    try:
        loader = nodelist.pop(
            nodelist.index(
                next(node for node in nodelist if isinstance(node, FallbackNode))
            )
        )
    except StopIteration:
        loader = FallbackNode()

    parser.delete_first_token()

    return SuspenseNode(loader, nodelist, async_context_keys)


class SuspenseNode(template.Node):
    def __init__(self, loading, nodelist, async_context_keys):
        self.loading = loading
        self.nodelist = nodelist
        self.async_context_keys = async_context_keys

    def render(self, context):
        if context["is_async"]:
            uid, task = create_async(
                self.nodelist, copy(context), self.async_context_keys
            )
        else:
            uid, task = create(self.nodelist, copy(context))
        request = context["request"]
        if not hasattr(request, "_suspense"):
            request._suspense = []
        request._suspense.append(task)

        return template.loader.render_to_string(
            'suspense/loader.html',
            {'uid': uid, 'loading': self.loading.render(context)},
        )


@register.tag(name="fallback")
def fallback_tag(parser, token):
    nodelist = parser.parse(("endfallback",))
    parser.delete_first_token()

    return FallbackNode(nodelist)


class FallbackNode(template.Node):
    def __init__(self, nodelist=None):
        self.nodelist = nodelist

    def render(self, context):
        if self.nodelist:
            return self.nodelist.render(context)
        return ''


@register.simple_tag(name="webkit_extra_invisible_bytes", takes_context=True)
def webkit_extra_invisible_bytes(context, byte_count=200):
    agent = context["request"].META.get('HTTP_USER_AGENT', '')
    if byte_count > 0 and 'AppleWebKit' in agent:
        zero_width_spaces = byte_count * "\u200b"
        return mark_safe(f'<div style="width: 0; height: 0;">{zero_width_spaces}</div>')
    return ''
