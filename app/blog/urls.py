from django.urls import path
from . import views
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from django.contrib.auth.decorators import login_required

router = DefaultRouter()


urlpatterns = [
    path("", views.StartingPage.as_view(), name='starting-page'),
    path("posts", views.AllPosts.as_view(), name='posts-page'),
    path("posts/<slug:slug>", views.PostDetails.as_view(), name='posts-detail-page'),
    path("add-post", views.AddPost.as_view() , name='add-post'),
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
    path("profile/", views.ProfileView.as_view()  ,
         name="profile"),
    path("serial_user", views.BlogListUser.as_view(), name="serial-view-user"),
    path('edit/<int:pk>/', views.edit_blog_post   , name='edit_blog_post'),
    path('get_user_from_token/', views.GetUserFromTokenView.as_view(), name='get_user_from_token'),
]

# urlpatterns += router.urls