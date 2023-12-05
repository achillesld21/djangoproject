from django.contrib import admin
from .models import user, blog_post

# Register your models here.

admin.site.register(user)
admin.site.register(blog_post)
