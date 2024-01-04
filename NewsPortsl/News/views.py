from django.core.cache import cache
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect, render
from .models import Post, Category
from .filters import *
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from .tasks import *

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
    def get_object(self, *args, **kwargs):
        obj = cache.get(f'Post-{self.kwargs["pk"]}', None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'Post-{self.kwargs["pk"]}', obj)

        return obj

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


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('News.add_post', 'News.edit_post')
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        send_message.delay()
        post = form.save(commit=False)
        if 'news' in self.request.path:
            post.type = 'NW'
        else:
            post.type = 'AR'
        return super().form_valid(form)

class PostEdit(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('News.add_post', 'News.edit_post')
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_premium'] = not self.request.user.groups.filter(name='author').exists()
        return context

class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
        return context

@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/news')

class CategoriesList(ListView):
    model = Category
    ordering = 'name'
    template_name = 'categories_list.html'
    context_object_name = 'categories'
    paginate_by = 10


@login_required()
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    return render(request, 'subscribe.html', {'category': category})