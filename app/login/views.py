from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm
from blog import views
from blog.auth import generate_access_token,generate_refresh_token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from my_blog_site.serializers import UserLoginSerializer,UserSerializer
from django.views.generic import TemplateView
from rest_framework.permissions import AllowAny,IsAuthenticated




class UserLoginView(APIView):
	authentication_classes = []  # An empty list means no authentication is required
	permission_classes = [AllowAny]  # Allow any user, including unauthenticated ones
	
	def post(self, request, *args, **kwargs):
		serializer = UserLoginSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		username = serializer.validated_data['username']
		password = serializer.validated_data['password']
		user = authenticate(username=username, password=password)
		
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

	template_name = "login/login.html"



class LogoutAPIView(APIView):
	authentication_classes = []
	permission_classes = []
	def get(self, request):
		return Response({'detail': 'Logout successful'}, status=status.HTTP_200_OK)
	

class RegisterUser(TemplateView):

	template_name = "login/register_user.html"

class RegisterUserAPIView(APIView):
	authentication_classes = []  # An empty list means no authentication is required
	permission_classes = [AllowAny]  # Allow any user, including unauthenticated ones
	def post(self, request, *args, **kwargs):
		serializer = UserSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)