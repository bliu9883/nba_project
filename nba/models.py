from django.db import models

# Create your models here.
class Team(models.Model):
	team_id = models.IntegerField()
	team_name = models.CharField(max_length=200)
	tri_code = models.CharField(max_length=200)

	def __str__(self):
		return self.team_name

class Players(models.Model):
	player_id = models.IntegerField()
	player_name = models.CharField(max_length=200)
	team = models.ForeignKey(Team, on_delete=models.CASCADE)

	def __str__(self):
		return self.player_name