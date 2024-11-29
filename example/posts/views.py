from django.shortcuts import get_object_or_404, render

from suspense.shortcuts import render as suspense_render
from suspense.views import SuspenseTemplateView

from .models import Post


def posts(request):
    posts = Post.objects.all()

    return suspense_render(request, 'posts/all.html', {'posts': posts})


def post(request, slug):
    post = get_object_or_404(Post, slug=slug)

    return render(request, 'posts/post.html', {'post': post})


class PostTemplateView(SuspenseTemplateView):
    template_name = 'posts/all.html'

    def get_context_data(self, **kwargs):
        return {'posts': Post.objects.all()}
