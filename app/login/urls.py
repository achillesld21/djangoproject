from django.urls import path
from . import views



urlpatterns = [
    path('login_user', views.login_user.as_view(), name="login"),
    path('logout_user', views.UserLogoutview.as_view(), name='logout'),
    path('register_user', views.register_user, name='register_user'),
    path('login_api', views.UserLoginView.as_view(), name='api_login'),
]
