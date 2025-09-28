from django.contrib import admin
from .models import DispatchInfo, User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "is_active", "is_staff")


@admin.register(DispatchInfo)
class DispatchInfoAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "label", "city", "is_default", "updated_at")
    list_filter = ("is_default", "city", "country")
    search_fields = ("user__email", "user__username", "label", "city")
