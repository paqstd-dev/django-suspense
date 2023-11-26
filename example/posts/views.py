from django.shortcuts import get_object_or_404, render

from .models import Post


def posts(request):
    posts = Post.objects.all()

    return render(request, 'posts/all.html', {'posts': posts})


def post(request, slug):
    post = get_object_or_404(Post, slug=slug)

    return render(request, 'posts/post.html', {'post': post})
