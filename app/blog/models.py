from django.db import models
from django.utils.text import slugify

# Create your models here.
class user(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email_address = models.EmailField()

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name()


class blog_post(models.Model):
    category = models.CharField(max_length=20)
    heading = models.CharField(max_length=50)
    content = models.TextField()
    image = models.ImageField(upload_to="images")
    user = models.ForeignKey(
        user, on_delete=models.SET_NULL, null=True, related_name="posts"
    )
    posted_date = models.DateField(auto_now_add=True)
    slug = models.SlugField(unique=True, db_index=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.heading)

        super().save(*args, **kwargs)