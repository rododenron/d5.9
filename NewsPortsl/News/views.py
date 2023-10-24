from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from .models import Post
from .filters import *
from .forms import PostForm
from django.contrib.auth.decorators import login_required

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


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('News.add_post', 'News.edit_post')
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
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
