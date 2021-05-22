from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView

from .models import Post

from django.views.generic import DetailView
# Create your views here.

#a queryset is collection of database queries to retrieve objects from the database
class PostListView(ListView):
    model = Post
    paginate_by = 3
    context_object_name = 'posts' #default post_list
  





def post_detail(request, year, month, day, post):

    post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)

    return render(request, 'blog/post_detail.html',  {'post': post})
                  
                 


class PostDetailView(DetailView):
    model = Post