from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


# Create your models here.


class blog_post(models.Model):
    category = models.CharField(max_length=20)
    heading = models.CharField(max_length=50)
    content = models.TextField()
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    User = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="posts"
    )
    username = models.CharField(max_length=50, blank=True, null=True)
    posted_date = models.DateField(auto_now_add=True)
    slug = models.SlugField(db_index=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.heading)

        super().save(*args, **kwargs)
