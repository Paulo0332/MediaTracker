from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user_media.models import UserMediaList
from .models import CustomUser

# Register your models here.
class UserMediaListInline(admin.TabularInline):
    model = UserMediaList
    extra = 0
    raw_id_fields = ('media',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
    
        return qs.select_related('media')

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    inlines = [UserMediaListInline]
    
    list_display = ("username", "email", "is_staff")
    list_filter = ("is_staff",)
    