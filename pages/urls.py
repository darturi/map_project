from django.urls import path

from .views import HomePageView, ProfileView

urlpatterns = [
    path("profile/", ProfileView.as_view(), name="profile"),
    path("", HomePageView.as_view(), name="home"),
]
