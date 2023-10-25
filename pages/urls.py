from django.urls import path

from .views import (
    HomePageView,
    ProfileView,
    AddressDetailView,
    CommentDelete,
    MyPinsView,
)

urlpatterns = [
    path("<int:pk>/", AddressDetailView.as_view(), name="address_detail"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("my_pins/", MyPinsView.as_view(), name="my_pins"),
    path("<int:pk>/delete/", CommentDelete.as_view(), name="comment_delete"),
    path("", HomePageView.as_view(), name="home"),
]
