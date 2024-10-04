from django.contrib import admin
from users.models import User
from django.utils.html import format_html


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'data_joined', 'get_image')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'data_joined', 'first_name', 'last_name')

    def get_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" class="rounded-circle" style="width: 50px; height: 50px;" />',
                               obj.image.url)
        return format_html('<span> No image </span>')

    get_image.short_description = 'Image'
