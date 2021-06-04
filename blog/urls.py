from django.urls import path
from . import views
from .feeds import LatestPostsFeed
from django.views.generic import TemplateView

app_name = 'blog'
urlpatterns = [
   # path('', views.post_list, name='post_list'),
    path('blogposts',views.PostListView.as_view(), name = 'post_list'),
    path('', views.index, name='home_page'),

    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
                views.post_detail,
                name='post_detail'),

    
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('search/', views.post_search, name='post_search'),
    path('contacts/', TemplateView.as_view(template_name='contact.html'), name='contacts')
    


]