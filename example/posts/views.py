import asyncio

from django.shortcuts import get_object_or_404, render

from suspense.shortcuts import async_render, render as suspense_render
from suspense.views import AsyncSuspenseTemplateView, SuspenseTemplateView

from .models import Post, SlowPost


def posts(request):
    posts = SlowPost.objects.all()

    return suspense_render(request, 'posts/all.html', {'posts': posts})


def post(request, slug):
    post = get_object_or_404(SlowPost, slug=slug)

    return render(request, 'posts/post.html', {'post': post})


class PostTemplateView(SuspenseTemplateView):
    template_name = 'posts/all.html'

    def get_context_data(self, **kwargs):
        return {'posts': Post.objects.all()}


async def async_posts(request):
    async def fetch_posts():
        await asyncio.sleep(5)
        return [a async for a in Post.objects.all()]

    return async_render(
        request, 'posts/all.html', {'posts': asyncio.create_task(fetch_posts())}
    )


class AsyncPostTemplateView(AsyncSuspenseTemplateView):
    template_name = 'posts/all.html'

    def get_context_data(self, **kwargs):
        async def fetch_posts():
            await asyncio.sleep(5)
            return [a async for a in Post.objects.all()]

        return {'posts': asyncio.create_task(fetch_posts())}
