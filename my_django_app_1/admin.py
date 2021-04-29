from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, LocalSettings, Customer

# Register your models here.
admin.site.register(User, UserAdmin)
# admin.site.register(LocalSettings)
admin.site.register(Customer)


@admin.register(LocalSettings)
class UserAdmin(admin.ModelAdmin):
    list_display = ['record_type', 'value']
    list_filter = ['record_type']