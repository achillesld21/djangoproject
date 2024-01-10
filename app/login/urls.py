from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView



urlpatterns = [
    path('login_user', views.LoginUser.as_view(), name="login"),
    path('register_user', views.RegisterUser.as_view(), name='register_user'),
    path('api/register', views.RegisterUserAPIView.as_view(), name='register_user_api'),
    path('login_api', views.UserLoginView.as_view(), name='api_login'),
    path('api/logout/', views.LogoutAPIView.as_view(), name='logout'),
]
