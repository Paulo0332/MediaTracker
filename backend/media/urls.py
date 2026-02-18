from django.urls import path
from .views import MediaListView

app_name = 'media'

urlpatterns = [
    path('',MediaListView.as_view(), name='list'),
]
