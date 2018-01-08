from django.contrib import admin

from .models import Team, Player

# Register your models here.
class TeamAdmin(admin.ModelAdmin):
	list_display = ['id', 'team_name', 'tri_code', 'color', 'conference', 'division', 'wins', 'losses']
	ordering = ('team_name',)
	
class PlayerAdmin(admin.ModelAdmin):
	list_display = ['id', 'first_name', 'last_name', 'team']
	ordering = ('team', 'last_name')
	
admin.site.register(Team, TeamAdmin)
admin.site.register(Player, PlayerAdmin)