from django.db import models

# Create your models here.
class Signup(models.Model):
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class Gallery(models.Model):
    photo = models.ImageField(blank=True, null =True)
    featured = models.BooleanField(default=False)

class Background(models.Model):
    picture = models.ImageField(blank=True, null =True)
    featured = models.BooleanField(default=False)