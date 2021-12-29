from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from qux.seo.mixin import SEOMixin
from .models import Newsitem
from .forms import NewsitemForm


class NewsListView(SEOMixin, ListView):
    model = Newsitem
    queryset = Newsitem.objects.all()
    template_name = 'newsfeed/list.html'


class NewsAdminListView(SEOMixin, ListView):
    model = Newsitem
    template_name = 'newsfeed/admin.html'


class NewsCreateView(SEOMixin, CreateView):
    model = Newsitem
    form_class = NewsitemForm
    template_name = 'newsfeed/create.html'
    extra_context = {
        'title': '<span>Newsitem</span>'
                 '<i class="fas fa-angle-right px-2"></i>'
                 '<span>Add</span>'
    }


class NewsItemView(SEOMixin, DetailView):
    model = Newsitem
    template_name = 'newsfeed/item.html'

    def get_object(self, queryset=None):
        if 'pk' in self.kwargs:
            obj = self.model.objects.get_or_none(id=self.kwargs['pk'])
        elif 'slug' in self.kwargs:
            obj = self.model.objects.get_or_none(slug=self.kwargs['slug'])
        else:
            obj = None

        return obj


class NewsItemEditView(SEOMixin, UpdateView):
    model = Newsitem
    form_class = NewsitemForm
    template_name = 'newsfeed/edit.html'
    extra_context = {
        'title': '<span>Newsitem</span>'
                 '<i class="fas fa-angle-right px-2"></i>'
                 '<span>Edit</span>'
    }


class NewsItemDeleteView(SEOMixin, DeleteView):
    model = Newsitem
    template_name = 'newsfeed/delete.html'


# class UserInfoView(SEOMixin, DetailView):
