from django.contrib import admin
from user_media.models import UserMediaList 

# Register your models here.

@admin.register(UserMediaList)
class UserMediaListAdmin(admin.ModelAdmin):
    @admin.display(description="User")
    def get_user_username(self,obj):
        return obj.user.username
    
    @admin.display(ordering='media__title', description="Media Title")
    def get_media_title(self,obj):
        return obj.media.title
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
    
        return qs.select_related('user','media')
    
    list_display = ('get_user_username', 'get_media_title', "status", "rating")
    list_filter = ("status", "rating")
    search_fields = ("media__title",)
    