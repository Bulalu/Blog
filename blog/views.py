from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail

from .models import Post
from .forms import EmailPostForm

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

