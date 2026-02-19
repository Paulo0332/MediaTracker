from django.shortcuts import render
from django.views.generic import ListView,DetailView
from media.models import Media
# Create your views here.

class MediaListView(ListView):
    model = Media
    context_object_name = "all_media"
    ordering = "title"
    template_name = "media/media_list.html"

class MediaDetailView(DetailView):
    model = Media
    context_object_name = "media"
    template_name = "media/media_detail.html"

    
    