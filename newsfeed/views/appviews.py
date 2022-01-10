from django.urls import reverse
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView
from django.views.generic import RedirectView

from qux.seo.mixin import SEOMixin
from ..forms import NewsitemForm
from ..models import Newsitem
from qux.utils.urls import MetaURL
from django.http.response import JsonResponse
from django.contrib.auth.models import User


class NewsItemListView(SEOMixin, ListView):
    model = Newsitem
    queryset = Newsitem.objects.all()
    template_name = "newsfeed/list.html"

    def get_queryset(self):
        creator = self.kwargs.get("creator", None)
        if creator:
            creator = User.objects.get(username__iexact=creator)
        result = self.queryset.filter(creator=creator)
        return result

    def post(self, request, *args, **kwargs):
        creator = self.kwargs.get("creator", None)
        if creator:
            creator = User.objects.get(username__iexact=creator)

        url = request.POST.get("url", None)
        if url:
            metaurl = MetaURL()
            metaurl.url = url
            metadata = metaurl.load()

            if type(metadata) is JsonResponse:
                siteurl = url
            else:
                siteurl = metadata.get("url", url)

            n = Newsitem.objects.get_or_none(url=siteurl, creator=creator)

            if n is None:
                n = Newsitem()
                n.url = siteurl
                n.domain = metaurl.domain
                n.title = metadata.get("title", None)
                n.description = metadata.get("description", None)
                n.image = metadata.get("image", None)
                if request.user.is_authenticated and request.user == creator:
                    n.creator = request.user

                n.save(preloaded=True)

        if creator:
            return redirect(reverse("newsfeed:list_user", kwargs={"creator": creator}))
        else:
            return redirect(reverse("newsfeed:list"))


class NewsAdminListView(SEOMixin, ListView):
    model = Newsitem
    template_name = "newsfeed/admin.html"


class NewsItemCreateView(SEOMixin, CreateView):
    model = Newsitem
    form_class = NewsitemForm
    template_name = "newsfeed/create.html"
    extra_context = {
        "title": "<span>Newsitem</span>"
        '<i class="bi bi-chevron-right px-2"></i>'
        "<span>Add</span>"
    }


class NewsItemView(SEOMixin, DetailView):
    model = Newsitem
    template_name = "newsfeed/item.html"

    def get_object(self, queryset=None):
        if "pk" in self.kwargs:
            obj = self.model.objects.get_or_none(id=self.kwargs["pk"])
        else:
            obj = None

        return obj


class NewsItemRedirectView(SEOMixin, RedirectView):
    model = Newsitem

    def get_redirect_url(self, *args, **kwargs):
        if "slug" in self.kwargs:
            obj = self.model.objects.get_or_none(slug=self.kwargs["slug"])
        else:
            return reverse("newsfeed:list")

        if obj is None:
            obj = self.model.objects.get_or_none(short_url=self.kwargs["slug"])

        if obj is None:
            return reverse("newsfeed:list")

        return obj.url


class NewsItemEditView(SEOMixin, UpdateView):
    model = Newsitem
    form_class = NewsitemForm
    template_name = "newsfeed/edit.html"
    extra_context = {
        "title": "<span>Newsitem</span>"
        '<i class="bi bi-chevron-right px-2"></i>'
        "<span>Edit</span>"
    }


class NewsItemDeleteView(SEOMixin, DeleteView):
    model = Newsitem
    success_url = "/"


# class UserInfoView(SEOMixin, DetailView):
