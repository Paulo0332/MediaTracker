from django.urls import path
from .views import MediaListView,MediaDetailView

app_name = 'media'

urlpatterns = [
    path('', MediaListView.as_view(), name='media-list'),
    path('<int:pk>/', MediaDetailView.as_view(), name='media-detail'),
]
