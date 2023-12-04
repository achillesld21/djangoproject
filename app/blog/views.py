from django.shortcuts import render
from .models import blog_post
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from .models import blog_post
from .forms import create_blog
from django.views import View

# Create your views here.

class AddPost(CreateView):
    model = blog_post
    form_class = create_blog
    template_name = "blog/add-post.html"
    success_url = "/"

class StartingPage(ListView):
    template_name = "blog/index.html"
    model = blog_post
    ordering = ["-posted_date"]
    context_object_name = "posts"
    

class AllPosts(ListView):
    template_name = "blog/all-posts.html"
    model = blog_post
    ordering = ["-posted_date"]
    context_object_name = "posts"


class PostDetails(View):
    def get(self,request,slug):
        post = blog_post.objects.get(slug=slug)
        context = {
            'post': post,
         }
        return render(request, "blog/post-detail.html", context)