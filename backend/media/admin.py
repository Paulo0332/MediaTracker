from django.contrib import admin
from media.models import Media

# Register your models here.
@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ("title","creator","media_type","release_date")
    list_filter = ("media_type",)
    search_fields = ("title","creator")
