from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Passenger


class PassengerInline(admin.StackedInline):
    model = Passenger
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = [
        PassengerInline,
    ]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
