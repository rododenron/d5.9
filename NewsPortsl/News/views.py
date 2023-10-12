from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post

# Create your views here.

class PostsList(ListView):
    model = Post
    ordering = '-date_time'
    template_name = 'Posts.html'
    context_object_name = 'posts'

class PostsDetail(DetailView):
    model = Post
    template_name = 'Post.html'
    context_object_name = 'post'
