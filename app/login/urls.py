from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView



urlpatterns = [
    path('login_user', views.login_user.as_view(), name="login"),
    path('register_user', views.register_user, name='register_user'),
    path('login_api', views.UserLoginView.as_view(), name='api_login'),
    path('api/logout/', views.LogoutAPIView.as_view(), name='logout'),
]
