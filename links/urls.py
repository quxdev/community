from django.urls import path

from .views.appviews import *

app_name = "links"

# u = user
# l = link
# x = short_url

urlpatterns = [
    path("", LinkHomeView.as_view(), name="home"),
    path("admin/", NewsAdminListView.as_view(), name="admin"),
    path("new/", LinkCreateView.as_view(), name="new"),
    path("u/<str:creator>/", LinkListView.as_view(), name="list"),
    path("u/<str:creator>/<str:tag>/", LinkListView.as_view(), name="tag"),
    path("l/<slug:slug>/", LinkView.as_view(), name="view"),
    path("l/<slug:slug>/edit/", LinkEditView.as_view(), name="edit"),
    path("l/<slug:slug>/delete/", LinkDeleteView.as_view(), name="delete"),
    # path("x/<str:short_url>/", LinkRedirectView.as_view(), name="short_url"),
    path("<slug:slug>/", LinkRedirectView.as_view(), name="slug"),
]
