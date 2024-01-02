from django.urls import path
from django.views.decorators.cache import cache_page

# Импортируем созданное нами представление
from .views import PostsList, PostDetail, PostSearch, PostCreate, PostEdit, PostDelete, upgrade_me, CategoriesList, \
   subscribe

urlpatterns = [
   path('', cache_page(60)(PostsList.as_view()), name='post_list'),
   path('<int:pk>', cache_page(300)(PostDetail.as_view()), name='post_detail'),
   path('search', PostSearch.as_view(), name='post_search'),
   path('create', PostCreate.as_view(), name='post_create'),
   path('<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('upgrade', upgrade_me, name='upgrade'),
   path('categories', CategoriesList.as_view(), name='categories'),
   path('categories/<int:pk>', subscribe, name='subscribe'),
]