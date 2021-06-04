from blog.templatetags.blog_tags import latest_posts
from django.contrib.postgres import search
from django.db.models import query
from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

from .models import Post, Category
from marketing.models import Signup, Gallery, Background
from .forms import  CommentForm, SearchForm

from django.views.generic import DetailView
# Create your views here.




def index(request):
    queryset = Post.objects.filter(featured=True)[:3]
    latest_posts = Post.objects.order_by('-publish') [:3]
    gallery = Gallery.objects.filter(featured=True)
    #naive approach on selecting the bg photo need to update it
    background = Background.objects.filter(featured=True)
    bg2 = background[0].picture
    bg1 = background[1].picture
    
    if request.method == "POST":
        email = request.POST["email"]
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()

    ctx ={
        'queryset':queryset,
        'latest_posts':latest_posts,
        'gallery':gallery,
        'bg1':bg1,
        'bg2':bg2
        
    }
    return render(request, 'index.html', ctx)

class PostListView(ListView):
    queryset = Post.objects.all()
    paginate_by = 4
    template_name ='blog.html'
    context_object_name = 'posts' #default post_list
    


def post_detail(request, year, month, day, post):

    post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    

    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return redirect(post.get_absolute_url())
            
      
    else:
        comment_form = CommentForm()  

    ctx = {
        'post':post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form

    }

    return render(request, 'post.html',  ctx)


                



def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', 'body', 'content')
            search_query = SearchQuery(query)
            results = Post.objects.annotate(
                    search=search_vector,
                    rank=SearchRank(search_vector,search_query)
                ).filter(search=search_query).order_by('-rank')

    ctx = {
        'form':form,
        'query':query,
        'results':results,
    }
    return render(request, 'blog/post_search.html', ctx)





 