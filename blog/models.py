from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from tinymce import HTMLField

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)
  
    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS_CHOICES =(
        ('draft', 'Draft'),
        ('published', 'Published')
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,unique_for_date='publish')
    body = models.TextField()
    content = HTMLField('Content')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    status = models.CharField(max_length=200, choices=STATUS_CHOICES, default='draft')
    category_count = models.IntegerField(default=0)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    thumbnail = models.ImageField()
    category = models.ManyToManyField(Category)
    previous_post = models.ForeignKey('self',related_name='previous', on_delete=models.SET_NULL, blank=True, null=True)
    next_post = models.ForeignKey('self', related_name='next', on_delete=models.SET_NULL, blank=True, null=True)
    featured = models.BooleanField(default=False)

    class Meta:
        ordering = ('-publish',) #most recent publishes to appear first
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                            args=[self.publish.year,
                            self.publish.month,
                            self.publish.day, self.slug])

    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=50)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'

        

    


