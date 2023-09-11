from django.urls import path

from .views import HomePageView, ProfileView, AddressDetailView

urlpatterns = [
    path("<int:pk>/", AddressDetailView.as_view(), name="address_detail"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("", HomePageView.as_view(), name="home"),
]
