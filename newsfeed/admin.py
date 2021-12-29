from django.contrib import admin

from qux.models import CoreModelAdmin
from .models import Newsitem


class NewsitemAdmin(CoreModelAdmin):
    list_display = ('id', 'creator', 'dtm_created', 'slug',) + \
                   CoreModelAdmin.list_display
    search_fields = ('id', 'author__username', 'date', 'titke', 'slug',)


admin.site.register(Newsitem, NewsitemAdmin)
