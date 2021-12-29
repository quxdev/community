from django.urls import reverse
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView
from django.views.generic import RedirectView
from django.views.generic import TemplateView

from qux.seo.mixin import SEOMixin
from ..forms import LinkForm
from ..models import Link
from qux.utils.urls import MetaURL
from django.http.response import JsonResponse
from django.contrib.auth.models import User


class LinkHomeView(SEOMixin, TemplateView):
    template_name = "links/_link.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse("links:list", kwargs={"creator": request.user}))
        else:
            return render(request, self.template_name)


class LinkListView(SEOMixin, ListView):
    model = Link
    queryset = Link.objects.all()
    template_name = "links/list.html"

    def get_queryset(self):
        user = self.request.user

        creator = self.kwargs.get("creator", None)
        if creator is None:
            if user.is_authenticated:
                creator = user

        if creator:
            creator = User.objects.get(username__iexact=creator)

            result = self.queryset.filter(creator=creator)
            if creator != user:
                result = result.exclude(is_shared=False)

            tag = self.kwargs.get("tag", None)
            if creator and tag:
                result = result.filter(tags__icontains=tag)

            print(result)

        else:
            result = self.queryset.filter(creator__isnull=True)

        return result

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        creator = self.kwargs.get("creator", None)
        if creator:
            data["creator"] = creator

        return data

    @staticmethod
    def post(request, *args, **kwargs):
        user = request.user if request.user.is_authenticated else None

        url = request.POST.get("url", None)
        if url:
            metaurl = MetaURL()
            metaurl.url = url
            metadata = metaurl.load()

            if type(metadata) is JsonResponse:
                siteurl = url
            else:
                siteurl = metadata.get("url", url)

            n = Link.objects.get_or_none(url=siteurl, creator=user)

            if n is None:
                n = Link()
                n.url = siteurl
                n.domain = metaurl.domain
                n.type = metadata.get("type", "website")
                n.title = metadata.get("title", None)
                n.description = metadata.get("description", None)
                n.image = metadata.get("image", None)
                if user:
                    n.creator = user

                n.save(preloaded=True)

        if user:
            return redirect(reverse("links:list", kwargs={"creator": user}))
        else:
            return redirect(reverse("links:home"))


class NewsAdminListView(SEOMixin, ListView):
    model = Link
    template_name = "links/admin.html"


class LinkCreateView(SEOMixin, CreateView):
    model = Link
    form_class = LinkForm
    template_name = "links/create.html"
    extra_context = {
        "title": "<span>URL</span>"
        '<i class="bi bi-chevron-right px-2"></i>'
        "<span>Add</span>"
    }


class LinkView(SEOMixin, DetailView):
    model = Link
    template_name = "links/item.html"

    def get_object(self, queryset=None):
        if "slug" in self.kwargs:
            obj = self.model.objects.get_or_none(slug=self.kwargs["slug"])
        else:
            obj = None

        return obj


class LinkRedirectView(SEOMixin, RedirectView):
    model = Link

    def get_redirect_url(self, *args, **kwargs):
        if "slug" in self.kwargs:
            obj = self.model.objects.get_or_none(slug=self.kwargs["slug"])
        else:
            return reverse("links:list")

        if obj is None:
            obj = self.model.objects.get_or_none(short_url=self.kwargs["slug"])

        if obj is None:
            return reverse("links:list")

        return obj.url


class LinkEditView(SEOMixin, UpdateView):
    model = Link
    form_class = LinkForm
    template_name = "links/edit.html"
    extra_context = {
        "title": "<span>URL</span>"
        '<i class="bi bi-chevron-right px-2"></i>'
        "<span>Edit</span>"
    }


class LinkDeleteView(SEOMixin, DeleteView):
    model = Link
    success_url = "/"


# class UserInfoView(SEOMixin, DetailView):
