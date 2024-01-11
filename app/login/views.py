"""
This module contains the views for the user authentication and authorization in the Django project.
"""

from django.contrib.auth import authenticate
from blog.auth import generate_access_token, generate_refresh_token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from my_blog_site.serializers import UserLoginSerializer, UserSerializer
from django.views.generic import TemplateView
from rest_framework.permissions import AllowAny


class UserLoginView(APIView):
    """
    API view for user login.

    Args:
        request (HttpRequest): The incoming request.

    Returns:
        Response: A JSON response containing the access and refresh tokens.

    Raises:
        ValidationError: If the request data is not valid.
        AuthenticationFailed: If the credentials are incorrect.

    """

    authentication_classes = []  # An empty list means no authentication is required
    permission_classes = [AllowAny]  # Allow any user, including unauthenticated ones

    def post(self, request, *args, **kwargs):
        """
        Authenticate the user and generate access and refresh tokens.

        Args:
            request (HttpRequest): The incoming request.

        Returns:
            Response: A JSON response containing the access and refresh tokens.

        Raises:
            AuthenticationFailed: If the credentials are incorrect.

        """
        # Validate user login data
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Authenticate user
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)

        # Generate tokens if authentication is successful
        if user is not None:
            refresh = generate_refresh_token(user)
            access_token = generate_access_token(user)
            return Response({
                'access_token': str(access_token),
                'refresh_token': str(refresh),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class LoginUser(TemplateView):
    """
    HTML template view for user login.

    Attributes:
        template_name (str): The path to the template file.

    """
    template_name = "login/login.html"


class LogoutAPIView(APIView):
    """
    API view for user logout.

    Args:
        request (HttpRequest): The incoming request.

    Returns:
        Response: A JSON response with a message indicating that the user has been logged out.

    """
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        """
        Logout the user.

        Args:
            request (HttpRequest): The incoming request.

        Returns:
            Response: A JSON response with a message indicating that the user has been logged out.

        """
        # Logout response
        return Response({'detail': 'Logout successful'}, status=status.HTTP_200_OK)


class RegisterUser(TemplateView):
    """
    HTML template view for user registration.

    Attributes:
        template_name (str): The path to the template file.

    """
    template_name = "login/register_user.html"


class RegisterUserAPIView(APIView):
    """
    API view for user registration.

    Args:
        request (HttpRequest): The incoming request.

    Returns:
        Response: A JSON response containing the newly created user.

    Raises:
        ValidationError: If the request data is not valid.

    """
    authentication_classes = []  # An empty list means no authentication is required
    permission_classes = [AllowAny]  # Allow any user, including unauthenticated ones

    def post(self, request, *args, **kwargs):
        """
        Register a new user.

        Args:
            request (HttpRequest): The incoming request.

        Returns:
            Response: A JSON response containing the newly created user.

        Raises:
            ValidationError: If the request data is not valid.

        """
        # Validate and save user registration data
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)