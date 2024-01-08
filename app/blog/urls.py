from django.urls import path
from . import views
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from django.contrib.auth.decorators import login_required

router = DefaultRouter()


urlpatterns = [
    path("", login_required(views.StartingPage.as_view(), login_url='login/login_user'), name='starting-page'),
    path("posts", login_required(views.AllPosts.as_view(), login_url='login/login_user'), name='posts-page'),
    path("posts/<slug:slug>", login_required(views.PostDetails.as_view(), login_url='login/login_user'), name='posts-detail-page'),
    path("add-post", login_required(views.AddPost.as_view(), login_url='login/login_user'), name='add-post'),
    path("createpost", views.CreateBlogPostApiView.as_view(),
         name="createpost"),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path("serial", views.BlogList.as_view(), name="serial-view"),
    path("serial/<int:pk>/", views.ReadBlogPostApiView.as_view(),
         name="serial-number"),
    path("addpost", views.AddPostViewApi.as_view(), name="addpost"),
    path("updatepost/<int:pk>", views.UpdateBlogPostApiView.as_view(),
         name="updatepost"),
    path("deletepost/<int:pk>", views.DeleteBlogPostApiView.as_view(),
         name="deletepost"),
    path("profile/", views.ProfileView.as_view(),
         name="profile"),
    path("serial_user", views.BlogListUser.as_view(), name="serial-view-user"),
]

# urlpatterns += router.urls