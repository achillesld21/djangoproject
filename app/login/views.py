from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm
from blog import views
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponseRedirect
from django.urls import reverse



def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			refresh = RefreshToken.for_user(user)
			access_token = str(refresh.access_token)
			request.session['refresh_token'] = str(refresh)
			redirect_url = reverse('starting-page')
			response = HttpResponseRedirect(redirect_url)
			response.set_cookie(key="jwt", value=access_token, httponly=True, max_age=3600)
			return response
		else:
			messages.success(request, ("There Was An Error Logging In, Try Again..."))	
			return redirect('login')	


	else:
		return render(request, 'login/login.html', {})

def logout_user(request):
	messages.success(request, ("You Were Logged Out!"))
	redirect_url = reverse('login')
	response = HttpResponseRedirect(redirect_url)
	response.delete_cookie('jwt')
	logout(request)
	return response


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