from django.contrib import admin
from django.core.exceptions import PermissionDenied
from .models import Profile

# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__email')

    def save_model(self, request, obj, form, change):
        # Prevent non-superusers from creating or editing doctor profiles
        if not request.user.is_superuser and obj.role == 'doctor':
            raise PermissionDenied("Only superusers can assign Doctor role.")
        super().save_model(request, obj, form, change)