from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post
from .filters import *

# Create your views here.

class PostsList(ListView):
    model = Post
    ordering = '-date_time'
    template_name = 'Posts.html'
    context_object_name = 'posts'
    paginate_by = 10


class PostsDetail(DetailView):
    model = Post
    template_name = 'Post.html'
    context_object_name = 'post'

class Search(ListView):
    model = Post
    ordering = '-date_time'
    template_name = 'Search.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context
