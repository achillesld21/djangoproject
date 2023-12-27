from django.shortcuts import render, redirect
from .models import blog_post
from django.views.generic.edit import CreateView
from django.views.generic import ListView,TemplateView
from .forms import CreateBlog
from django.views import View
from my_blog_site.serializers import BlogSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from django.utils.text import slugify
from django.contrib.auth import logout
import requests


# Create your views here.
class AddPost(View):
    template_name = "blog/add-post.html"

    def get(self, request, *args, **kwargs):
        form = CreateBlog()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = CreateBlog(request.POST)
        if form.is_valid():
            category = form.cleaned_data['category']
            heading = form.cleaned_data['heading']
            content = form.cleaned_data['content']
            image = form.cleaned_data['image']
            user = form.cleaned_data['User']


            # Send a POST request to the API with data as JSON
            api_data = {
                "category": category,
                "heading": heading,
                "content": content,
                "image": image,
                "User": user,      
                "slug": None
            }
            headers = {'Content-Type': 'application/json'}  # Specify JSON content type
            response = requests.post("http://0.0.0.0:8000/addpost", json=api_data, headers=headers)

            if response.status_code == 201:
                 return redirect('starting-page')
            else:
                return render(request, 'error.html', {'message': 'API request failed'})

        return render(request, self.template_name, {'form': form})


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


class StartingPage(TemplateView):
    template_name = "blog/index.html"


class AllPosts(TemplateView):
    template_name = "blog/all-posts.html"


class PostDetails(View):
    def get(self, request, slug):
        post = blog_post.objects.get(slug=slug)
        context = {
            'post': post,
        }
        return render(request, "blog/post-detail.html", context)

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('starting-page')

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
