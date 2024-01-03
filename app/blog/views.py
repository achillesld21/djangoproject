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
from django.contrib import messages
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.


class AddPost(View):
    template_name = "blog/add-post.html"

    def get(self, request, *args, **kwargs):
        token = request.COOKIES.get('jwt')
        form = CreateBlog()
        return render(request, self.template_name, {
            'form': form,
            'token': token
            })
    
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
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
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
        messages.success(request, ("You Were Logged Out!"))
        redirect_url = reverse('login')
        response = HttpResponseRedirect(redirect_url)
        response.delete_cookie('jwt')
        logout(request)
        return response

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
    def get(self, request, *args, **kwargs):
        auth_token = request.COOKIES.get('jwt')
        if not auth_token:
            return render(request, 'error.html', {'message': 'API request failed'})
        else:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CreateBlogPostApiView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
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

    def get(self, request, *args, **kwargs):
        auth_token = request.COOKIES.get('jwt')
        if not auth_token:
            return render(request, 'error.html', {'message': 'API request failed'})
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)


class UpdateBlogPostApiView(generics.RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    queryset = blog_post.objects.all()
    serializer_class = BlogSerializer
    lookup_field = 'pk'

    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.slug:
            instance.slug = slugify(instance.heading)


class DeleteBlogPostApiView(generics.RetrieveDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    queryset = blog_post.objects.all()
    serializer_class = BlogSerializer
    lookup_field = 'pk'
