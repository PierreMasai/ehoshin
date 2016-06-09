from django.contrib import admin
from .models import Team


class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_private', 'is_closed')

admin.site.register(Team, TeamAdmin)
