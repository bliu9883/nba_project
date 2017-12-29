from django.db import models
from django.utils import timezone
import datetime

# Create your models here.
class Team(models.Model):
	team_name = models.CharField(max_length=200)
	tri_code = models.CharField(max_length=200)
	color = models.CharField(max_length=20, default="")
	conference = models.CharField(max_length=30, default="")
	division = models.CharField(max_length=10, default="")
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.team_name
		
	def was_updated_recently(self):
		return self.updated_at >= timezone.now() - datetime.timedelta(days=30)

class Player(models.Model):
	first_name = models.CharField(max_length=200, default="")
	last_name = models.CharField(max_length=200, default="")
	team = models.ForeignKey(Team, on_delete=models.CASCADE)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.first_name + " " + self.last_name
		
	def was_updated_recently(self):
		return self.updated_at >= timezone.now() - datetime.timedelta(days=1)
		
class PlayerStats(models.Model):
	player = models.ForeignKey(Player, on_delete=models.CASCADE)
	points = models.CharField(max_length=10, default="0.0")
	rebounds = models.CharField(max_length=10, default="0.0")
	assists = models.CharField(max_length=10, default="0.0")
	updated_at = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return self.player
		
	def was_updated_recently(self):
		return self.updated_at >= timezone.now() - datetime.timedelta(days=1)