from django.contrib import admin
from .models import Background, Signup, Gallery
# Register your models here.


admin.site.register(Signup)

@admin.register(Gallery)
class PostAdmin(admin.ModelAdmin):
    list_display = ('photo','featured')
    list_filter = ('featured',)

@admin.register(Background)
class PostAdmin(admin.ModelAdmin):
    list_display = ('picture','featured')
    list_filter = ('featured',)

