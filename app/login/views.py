from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm
from blog import views
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from my_blog_site.serializers import UserLoginSerializer
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
			login(request, user)
			refresh = RefreshToken.for_user(user)
			return Response({
				'access_token': str(refresh.access_token),
				'refresh_token': str(refresh),
				}, status=status.HTTP_200_OK)
		else:
			return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class login_user(TemplateView):

	template_name = "login/login.html"


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        request.auth.delete() 

        return Response({'detail': 'Logout successful'}, status=status.HTTP_200_OK)


def register_user(request):
	if request.method == "POST":
		form = RegisterUserForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, ("Registration Successful!"))
			return redirect('login')
	else:
		form = RegisterUserForm()

	return render(request, 'login/register_user.html', {
		'form':form,
		})