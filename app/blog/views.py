from django.shortcuts import render
from .models import blog_post
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from .forms import CreateBlog
from django.views import View
from my_blog_site.serializers import BlogSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from django.utils.text import slugify


# Create your views here.
class AddPost(CreateView):

    model = blog_post
    form_class = CreateBlog
    template_name = "blog/add-post.html"
    success_url = "/home"


class AddPostViewApi(APIView):
    queryset = blog_post.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            heading = serializer.validated_data.get('heading')
            slug = serializer.validated_data.get('slug') or None
            if slug is None:
                slug = slugify(heading)
            serializer.save(slug=slug)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    def get(self, request, slug):
        post = blog_post.objects.get(slug=slug)
        context = {
            'post': post,
        }
        return render(request, "blog/post-detail.html", context)


# class BlogList(APIView):

#     def get(self, request, format=None):
#         blog = blog_post.objects.all()
#         serializer = BlogSerializer(blog, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         data = JSONParser().parse(request)
#         serializer = BlogSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors,
# status=status.HTTP_400_BAD_REQUEST)


class BlogList(generics.ListAPIView):
    queryset = blog_post.objects.all()
    serializer_class = BlogSerializer


class CreateBlogPostApiView(generics.ListCreateAPIView):
    queryset = blog_post.objects.all()
    serializer_class = BlogSerializer
    lookup_field = 'pk'

    def perform_create(self, serializer):
        instance = serializer.save()
        if not instance.slug:
            instance.slug = slugify(instance.heading)


class ReadBlogPostApiView(generics.RetrieveAPIView):
    queryset = blog_post.objects.all()
    serializer_class = BlogSerializer
    lookup_field = 'pk'


class UpdateBlogPostApiView(generics.RetrieveUpdateAPIView):
    queryset = blog_post.objects.all()
    serializer_class = BlogSerializer
    lookup_field = 'pk'

    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.slug:
            instance.slug = slugify(instance.heading)


class DeleteBlogPostApiView(generics.RetrieveDestroyAPIView):
    queryset = blog_post.objects.all()
    serializer_class = BlogSerializer
    lookup_field = 'pk'
