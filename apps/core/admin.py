from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserTeam


class UserTeamAdmin(admin.ModelAdmin):
    fields = ['name', 'owner', 'users', 'active']


admin.site.register(User, UserAdmin)
admin.site.register(UserTeam, UserTeamAdmin)

