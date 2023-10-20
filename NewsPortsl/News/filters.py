import django_filters
from django import template, forms
from .models import Post


register = template.Library()


@register.filter()
def censor(value):
   return f'{value.replace("a","*")}'


class PostFilter(django_filters.FilterSet):
    subject = django_filters.CharFilter(lookup_expr='icontains')
    author_id__user__username = django_filters.CharFilter(lookup_expr='icontains')
    date_time = django_filters.DateTimeFilter(widget=forms.DateTimeInput(attrs={'type': 'date'}), lookup_expr='date__gt', label='Post date greater than')


    class Meta:
       model = Post
       fields = ['subject', 'author_id__user__username', 'date_time']