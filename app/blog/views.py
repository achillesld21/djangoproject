from django.shortcuts import render, redirect, get_object_or_404
from .models import blog_post
from django.views.generic import TemplateView
from django.views import View
from my_blog_site.serializers import BlogSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from django.utils.text import slugify
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib import messages
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .authentication import JWTAuthentication
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import BlogPostForm
import jwt
from django.conf import settings


# Views are listed here.


# View for rendering the add-post.html page
class AddPost(TemplateView):
    template_name = "blog/add-post.html"
        

class AddPostViewApi(APIView):
    """
    API view for adding a new blog post.
    Requires JWT authentication and permission from authenticated users.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = blog_post.objects.all()

    def post(self, request, *args, **kwargs):
        # Deserialize the request data using the BlogSerializer
        serializer = BlogSerializer(data=request.data)

        # Check if the data is valid
        if serializer.is_valid():
            heading = serializer.validated_data.get('heading')
            slug = serializer.validated_data.get('slug') or None

            # Generate a slug if not provided in the request
            if slug is None:
                slug = slugify(heading)

            # Save the serialized data to create a new blog post
            serializer.save(slug=slug)

            # Return a success response with the serialized data
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # Return an error response with serializer errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StartingPage(TemplateView):
    """
    View for rendering the starting page.
    """
    template_name = "blog/index.html"


class AllPosts(TemplateView):
    """
    View for rendering a page displaying all blog posts.
    """
    template_name = "blog/all-posts.html"



class PostDetails(View):
    """
    View for displaying details of a specific blog post.
    """
    def get(self, request, slug):
        # Render the template with the context data
        return render(request, "blog/post-detail.html")


class LogoutView(View):
    """
    View for handling user logout.
    """
    def get(self, request):
        # Display a success message and redirect to the login page after logging out
        messages.success(request, ("You Were Logged Out!"))
        redirect_url = reverse('login')
        response = HttpResponseRedirect(redirect_url)
        response.delete_cookie('jwt')  # Delete the JWT cookie
        logout(request)
        return response


class BlogList(generics.ListAPIView):
    """
    API view for listing all blog posts.
    Requires JWT authentication and permission from authenticated users.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = blog_post.objects.all()
    serializer_class = BlogSerializer


class CreateBlogPostApiView(generics.ListCreateAPIView):
    """
    API view for creating a new blog post.
    Requires JWT authentication and admin user permission.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    queryset = blog_post.objects.all()
    serializer_class = BlogSerializer
    lookup_field = 'pk'

    def perform_create(self, serializer):
        # Set the slug using the heading if not provided in the request
        instance = serializer.save()
        if not instance.slug:
            instance.slug = slugify(instance.heading)


class ReadBlogPostApiView(generics.RetrieveAPIView):
    """
    API view for reading details of a specific blog post.
    Requires JWT authentication and permission from authenticated users.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = blog_post.objects.all()
    serializer_class = BlogSerializer
    lookup_field = 'slug'


class UpdateBlogPostApiView(generics.RetrieveUpdateAPIView):
    """
    API view for updating details of a specific blog post.
    Requires JWT authentication and permission from authenticated users.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = blog_post.objects.all()
    serializer_class = BlogSerializer
    lookup_field = 'pk'

    def perform_update(self, serializer):
        # Set the slug using the heading if not provided in the request
        instance = serializer.save()
        if not instance.slug:
            instance.slug = slugify(instance.heading)


class DeleteBlogPostApiView(generics.DestroyAPIView):
    """
    API view for deleting a specific blog post.
    Requires JWT authentication and permission from authenticated users.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = blog_post.objects.all()
    serializer_class = BlogSerializer
    lookup_field = 'pk'


class ProfileView(TemplateView):
    """
    View for rendering the user profile page.
    """
    template_name = "blog/profile.html"


class BlogListUser(generics.ListAPIView):
    """
    API view for listing blog posts of the current user.
    Requires JWT authentication and permission from authenticated users.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = BlogSerializer

    
    def get_queryset(self):
        # Return the queryset of blog posts belonging to the current user
        return blog_post.objects.filter(User=self.request.user)


def edit_blog_post(request, pk):
    """
    View for editing a specific blog post.
    """
    post = get_object_or_404(blog_post, pk=pk)

    if request.method == 'POST':
        # Process the form submission for editing the blog post
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog_post_detail', slug=post.slug)
    else:
        # Display the form for editing the blog post
        form = BlogPostForm(instance=post)

    return render(request, 'blog/edit-post.html', {'form': form, 'post': post})


class GetUserFromTokenView(APIView):
    """
    API view for retrieving user information from a JWT token.
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request, *args, **kwargs):
        # Get the JWT from the Authorization header
        authorization_header = request.headers.get('Authorization', '')
        if not authorization_header.startswith('Bearer '):
            return Response({'error': 'Invalid authorization header'}, status=status.HTTP_400_BAD_REQUEST)

        token = authorization_header.split(' ')[1]

        try:
            # Decode the token's payload
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

            # Assuming the user ID and username are stored in the payload
            user_id = payload.get('user_id')
            user_name = payload.get('user_name')

            if user_id is not None:
                # Return user information in the response
                return Response({
                    'user_id': user_id,
                    'user_name': user_name
                 }, status=status.HTTP_200_OK)
            else:
                # Return an error response for invalid or expired token
                return Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)

        except jwt.ExpiredSignatureError:
            # Return an error response for an expired token
            return Response({'error': 'Token has expired'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            # Return an error response for an invalid token
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
        

class GetUserDetailsView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, user_id, *args, **kwargs):
        try:
            # Retrieve the user object using the provided user ID
            user = User.objects.get(id=user_id)

            # Serialize the user object to include desired details
            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                # Add any other fields you want to include
            }

            return Response(user_data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)