from django.urls import path
from . import views
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = router.urls

urlpatterns += [
    path("", views.StartingPage.as_view(), name="starting-page"),
    path("posts", views.AllPosts.as_view(), name="posts-page"),
    path("posts/<slug:slug>", views.PostDetails.as_view(),
         name="posts-detail-page"),
    path("add-post", views.AddPost.as_view(), name="add-post"),
    path("serial", views.BlogList.as_view(), name="serial-view")
]
