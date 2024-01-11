from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    # User login view (HTML form)
    path('login_user', views.LoginUser.as_view(), name="login"),

    # User registration view (HTML form)
    path('register_user', views.RegisterUser.as_view(), name='register_user'),

    # User registration API endpoint
    path('api/register', views.RegisterUserAPIView.as_view(), name='register_user_api'),

    # User login API endpoint
    path('login_api', views.UserLoginView.as_view(), name='api_login'),

    # User logout API endpoint
    path('api/logout/', views.LogoutAPIView.as_view(), name='logout'),
]
