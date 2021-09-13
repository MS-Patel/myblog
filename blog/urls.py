from django.urls import path
from django.urls.resolvers import URLPattern

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.post_search, name='post_search'),
    path('category/<category>/', views.CatListView.as_view(), name='category'),
    path('<slug:post>/', views.post_single, name='post_single'),

]
