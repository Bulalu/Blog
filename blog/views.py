from django.contrib.postgres import search
from django.db.models import query
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

from .models import Post
from .forms import EmailPostForm, CommentForm, SearchForm

from django.views.generic import DetailView
# Create your views here.

#a queryset is collection of database queries to retrieve objects from the database
class PostListView(ListView):
    model = Post
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
            #create a new comment but dont save to db yet
            new_comment = comment_form.save(commit=False)
            #assign the current post to the comment
            new_comment.post = post
            #save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    ctx = {
        'post':post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form

    }

    return render(request, 'blog/post_detail.html',  ctx)


                
                 
def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            
            subject = f"{cd['name']} recommends you read " f"{post.title}"
            
            message = f"Read {post.title} at {post_url}\n\n" 
            f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'admin@myblog.com',
            [cd['to']])
            sent = True
    else:
        form = EmailPostForm()

    ctx= {'form':form, 'post':post, 'sent':sent}
    return render(request, 'blog/post_share.html', ctx)


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', 'body')
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



def index(request):
    return render(request, 'index.html')

def blogpost(request):
    return render(request, 'blog.html')

def postview(request):
    return render(request, 'post.html')


 