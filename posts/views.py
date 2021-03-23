from django.shortcuts import render
from django.views.generic import DetailView

from posts.models import Post


class PostView(DetailView):
    model = Post
    template_name = 'posts/details.html'
