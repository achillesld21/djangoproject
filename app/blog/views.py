from django.shortcuts import render, redirect
from .models import blog_post
from django.views.generic import TemplateView
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
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib.auth.mixins import UserPassesTestMixin,AccessMixin


# Create your views here.


class AddPost(View):
    template_name = "blog/add-post.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        current_user_name = request.user.username
        token = request.COOKIES.get('jwt')
        form = CreateBlog(User=user, Username=current_user_name)
        return render(request, self.template_name, {
            'form': form,
            'token': token
            })
    
    def post(self, request, *args, **kwargs):
        pass
        

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        user = self.request.user
        context['current_user'] = user

        token = request.COOKIES.get('jwt')
        context['token'] = token

        return context


class AllPosts(TemplateView):
    template_name = "blog/all-posts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        user = self.request.user
        context['current_user'] = user

        token = request.COOKIES.get('jwt')
        context['token'] = token

        return context


class PostDetails(View):
    def get(self, request, slug):
        post = blog_post.objects.get(slug=slug)
        context = {
            'post': post,
        }

        user = self.request.user
        context['current_user'] = user

        token = request.COOKIES.get('jwt')
        context['token'] = token
        
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


class BlogList(AccessMixin,generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = blog_post.objects.all()
    serializer_class = BlogSerializer

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
    
    def handle_no_permission(self):
        return HttpResponse("You do not have permission to access this page.", status=403)

class CreateBlogPostApiView(UserPassesTestMixin,generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    queryset = blog_post.objects.all()
    serializer_class = BlogSerializer
    lookup_field = 'pk'

    def perform_create(self, serializer):
        instance = serializer.save()
        if not instance.slug:
            instance.slug = slugify(instance.heading)
    
    def test_func(self):
        return self.request.user.is_superuser
    
    def handle_no_permission(self):
        return HttpResponse("You do not have permission to access this page.", status=403)


class ReadBlogPostApiView(AccessMixin,generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = blog_post.objects.all()
    serializer_class = BlogSerializer
    lookup_field = 'pk'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
    
    def handle_no_permission(self):
        return HttpResponse("You do not have permission to access this page.", status=403)



class UpdateBlogPostApiView(UserPassesTestMixin,generics.RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    queryset = blog_post.objects.all()
    serializer_class = BlogSerializer
    lookup_field = 'pk'

    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.slug:
            instance.slug = slugify(instance.heading)

    def test_func(self):
        return self.request.user.is_superuser
    
    def handle_no_permission(self):
        return HttpResponse("You do not have permission to access this page.", status=403)


class DeleteBlogPostApiView(UserPassesTestMixin,generics.RetrieveDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    queryset = blog_post.objects.all()
    serializer_class = BlogSerializer
    lookup_field = 'pk'

    def test_func(self):
        return self.request.user.is_superuser
    
    def handle_no_permission(self):
        return HttpResponse("You do not have permission to access this page.", status=403)