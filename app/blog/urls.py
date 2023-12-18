from django.urls import path
from . import views
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = router.urls

urlpatterns += [
    path("home", views.StartingPage.as_view(), name="starting-page"),
    path("posts", views.AllPosts.as_view(), name="posts-page"),
    path("posts/<slug:slug>", views.PostDetails.as_view(),
         name="posts-detail-page"),
    path("add-post", views.AddPost.as_view(), name="add-post"),
    path("createpost", views.CreateBlogPostApiView.as_view(),
         name="createpost"),
    path("serial", views.BlogList.as_view(), name="serial-view"),
    path("serial/<int:pk>/", views.ReadBlogPostApiView.as_view(),
         name="serial-number"),
    path("addpost", views.AddPostViewApi.as_view(), name="addpost"),
    path("updatepost/<int:pk>", views.UpdateBlogPostApiView.as_view(),
         name="updatepost"),
    path("deletepost/<int:pk>", views.DeleteBlogPostApiView.as_view(),
         name="deletepost")
]
