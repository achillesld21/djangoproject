from django.urls  import path
from . import views

urlpatterns = [
    path("", views.StartingPage.as_view(), name="starting-page"),
    path("posts", views.AllPosts.as_view(), name="posts-page"),
    path("posts/<slug:slug>", views.PostDetails.as_view(), name="posts-detail-page"),
    path("add-post", views.AddPost.as_view(), name="add-post" )
]