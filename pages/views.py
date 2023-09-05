from django.views.generic import TemplateView
from .models import Address
from django.views.generic.edit import CreateView


class HomePageView(TemplateView):
    template_name = "home.html"


class ProfileView(CreateView):
    template_name = "profile.html"
    model = Address
    fields = ["address"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[
            "mapbox_access_token"
        ] = "pk.eyJ1IjoiZGFuaWVsYXJ0dXJpIiwiYSI6ImNsbTJ2c2ZrYjF6bHozcm85d3phc2c1bTUifQ.Ubn6vNMeUlWJ4iBomj9_BA"
        context["addresses"] = Address.objects.all()
        return context
