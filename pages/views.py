from django.views.generic import TemplateView, FormView, DetailView
from .models import Address, Comment
from django.views import View
from django.views.generic.edit import CreateView, DeleteView
from django.urls import reverse_lazy, reverse
from .forms import CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.detail import SingleObjectMixin


class HomePageView(TemplateView):
    template_name = "home.html"


class ProfileView(CreateView):
    template_name = "profile.html"
    model = Address
    fields = ("address",)
    success_url = "/profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[
            "mapbox_access_token"
        ] = "pk.eyJ1IjoiZGFuaWVsYXJ0dXJpIiwiYSI6ImNsbTJ2c2ZrYjF6bHozcm85d3phc2c1bTUifQ.Ubn6vNMeUlWJ4iBomj9_BA"
        context["addresses"] = [model_obj for model_obj in Address.objects.all()]
        # context["addresses"] = Address.objects.all()
        # context["descriptions"] = Address.objects.all()
        return context


class CommentGet(LoginRequiredMixin, DetailView):
    model = Address
    template_name = "address_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context


class CommentPost(SingleObjectMixin, FormView):
    model = Address
    # passes form name to FormView
    form_class = CommentForm
    template_name = "address_detail.html"

    def post(self, request, *args, **kwargs):
        # gets address pk
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    # called when form validation is a success
    def form_valid(self, form):
        comment = form.save(commit=False)
        # specify the address the comment belongs to
        comment.address = self.object
        # specify the author of the comment by fetching user
        comment.author = self.request.user
        comment.save()
        return super().form_valid(form)

    # after comment is posted redirect to detail view of the address
    def get_success_url(self):
        address = self.object
        return reverse("address_detail", kwargs={"pk": address.pk})


"""
class CommentDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Address
    template_name = "address_delete.html"

    def get_success_url(self):
        address = self.object
        return reverse("address_detail", kwargs={"pk": address.pk})

    def test_func(self):
        return True
"""


class CommentDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "article_delete.html"
    # redirect to article list page upon success

    def get_success_url(self):
        address = self.object
        return reverse("address_detail", kwargs={"pk": address.pk})

    # Tests if the author of the article is the same as the user
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


# View for viewing one specific address in detail
class AddressDetailView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        view = CommentGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentPost.as_view()
        return view(request, *args, **kwargs)
