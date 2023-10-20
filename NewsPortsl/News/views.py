from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import *
from .forms import PostForm

# Create your views here.

class PostsList(ListView):
    model = Post
    ordering = '-date_time'
    template_name = 'Posts.html'
    context_object_name = 'posts'
    paginate_by = 10


class PostDetail(DetailView):
    model = Post
    template_name = 'Post.html'
    context_object_name = 'post'

class PostSearch(ListView):
    model = Post
    ordering = '-date_time'
    template_name = 'PostSearch.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):    
        queryset = super().get_queryset()        
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if 'news' in self.request.path:
            post.type = 'NW'
        else:
            post.type = 'AR'
        return super().form_valid(form)

class PostEdit(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'

class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')