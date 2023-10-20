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
    # date_time = django_filters.NumberFilter(field_name='date_time', lookup_expr='year')
    # date_time_gt = django_filters.NumberFilter(field_name='date_time', lookup_expr='year__gt')
    # date_time_lt = django_filters.DateTimeFilter(field_name='date_time', lookup_expr='date_time__lt')


    class Meta:
       model = Post
       fields = ['subject', 'author_id__user__username', 'date_time']