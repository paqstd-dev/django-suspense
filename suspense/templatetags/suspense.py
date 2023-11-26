from django import template

from suspense.futures import create

register = template.Library()


@register.tag(name="suspense")
def suspense_tag(parser, token):
    nodelist = parser.parse(("endsuspense",))

    try:
        loader = nodelist.pop(
            nodelist.index(
                next(node for node in nodelist if isinstance(node, FallbackNode))
            )
        )
    except StopIteration:
        loader = FallbackNode()

    parser.delete_first_token()

    return SuspenseNode(loader, nodelist)


class SuspenseNode(template.Node):
    def __init__(self, loading, nodelist):
        self.loading = loading
        self.nodelist = nodelist

    def render(self, context):
        uid = create(self.nodelist, context)

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
