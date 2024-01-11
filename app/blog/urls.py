from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

# Define a default router for REST framework
router = DefaultRouter()

urlpatterns = [
    # Homepage
    path("", views.StartingPage.as_view(), name='starting-page'),

    # View all posts
    path("posts", views.AllPosts.as_view(), name='posts-page'),

    # View details of a specific post using its slug
    path("posts/<slug:slug>", views.PostDetails.as_view(), name='posts-detail-page'),

    # Add a new post (HTML form)
    path("add-post", views.AddPost.as_view(), name='add-post'),

    # Create a new post using API
    path("createpost", views.CreateBlogPostApiView.as_view(), name="createpost"),

    # Logout view
    path('logout/', views.LogoutView.as_view(), name='logout'),

    # View all posts using Django Rest Framework's ListAPIView
    path("serial", views.BlogList.as_view(), name="serial-view"),

    # View details of a specific post using API
    path("serial/<slug:slug>/", views.ReadBlogPostApiView.as_view(), name="serial-number"),

    # Add a new post using API
    path("addpost", views.AddPostViewApi.as_view(), name="addpost"),

    # Update details of a specific post using API
    path("updatepost/<int:pk>", views.UpdateBlogPostApiView.as_view(), name="updatepost"),

    # Delete a specific post using API
    path("deletepost/<int:pk>", views.DeleteBlogPostApiView.as_view(), name="deletepost"),

    # User profile view
    path("profile/", views.ProfileView.as_view(), name="profile"),

    # View user-specific posts using Django Rest Framework's ListAPIView
    path("serial_user", views.BlogListUser.as_view(), name="serial-view-user"),

    # Edit a specific post using HTML form
    path('edit/<int:pk>/', views.edit_blog_post, name='edit_blog_post'),

    # Get user information from a token using API
    path('get_user_from_token/', views.GetUserFromTokenView.as_view(), name='get_user_from_token'),
]
