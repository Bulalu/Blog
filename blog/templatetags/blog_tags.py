from django.utils.safestring import mark_safe
from django.db.models import Count
from django import template
from ..models import Post, Category
import markdown
from django.db.models import Count


register = template.Library()

@register.simple_tag

def total_posts():
    return Post.objects.count()




@register.inclusion_tag('blog/post_latest_post.html')
def show_latest_posts(count=5):
    latest_posts  = Post.objects.order_by('-publish') [:count]
    return {'latest_posts': latest_posts}


@register.inclusion_tag('blog/get_category_list.html')

def get_category_count():
    queryset = Category.objects.all()
   # queryset = Post.objects.values('category__name').annotate(Count('category__name'))
     
    return {'queryset': queryset}
       
        




@register.simple_tag
def latest_posts():
    return Post.objects.order_by('-publish')[:3]
    
@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.objects.annotate(
                total_comments=Count('comments')
    ).order_by('-total_comments')[:count]



@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))

