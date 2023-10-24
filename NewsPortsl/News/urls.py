from django.urls import path
# Импортируем созданное нами представление
from .views import PostsList, PostDetail, PostSearch, PostCreate, PostEdit, PostDelete, upgrade_me


urlpatterns = [
   path('', PostsList.as_view(), name='post_list'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('search', PostSearch.as_view(), name='post_search'),
   path('create', PostCreate.as_view(), name='post_create'),
   path('<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('upgrade', upgrade_me, name='upgrade'),
]