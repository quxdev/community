from django.urls import path

from .views import *

app_name = 'news'

urlpatterns = [
    path('', NewsListView.as_view(), name='list'),
    path('admin/', NewsAdminListView.as_view(), name='admin'),
    path('new/', NewsCreateView.as_view(), name='new'),
    path('<int:pk>/', NewsItemView.as_view(), name='id'),
    path('<int:pk>/edit/', NewsItemEditView.as_view(), name='edit'),
    path('<int:pk>/delete/', NewsItemDeleteView.as_view(), name='delete'),
    path('<slug:slug>/', NewsItemView.as_view(), name='slug')
]
