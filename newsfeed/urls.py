from django.urls import path

from .views import *

app_name = 'newsfeed'

urlpatterns = [
    path('', NewsItemListView.as_view(), name='list'),
    path('admin/', NewsAdminListView.as_view(), name='admin'),
    path('new/', NewsItemCreateView.as_view(), name='new'),
    path('<int:pk>/', NewsItemView.as_view(), name='view'),
    path('<int:pk>/edit/', NewsItemEditView.as_view(), name='edit'),
    path('<int:pk>/delete/', NewsItemDeleteView.as_view(), name='delete'),
    path('<slug:slug>/', NewsItemRedirectView.as_view(), name='slug'),
]
