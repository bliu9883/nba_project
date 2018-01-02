from django.db import models
from django.utils import timezone
import datetime
from django.core.files import File
import urllib
import os

# Create your models here.
class Team(models.Model):
	team_name = models.CharField(max_length=200)
	tri_code = models.CharField(max_length=200)
	color = models.CharField(max_length=20)
	conference = models.CharField(max_length=30)
	division = models.CharField(max_length=10)
	updated_at = models.DateTimeField(auto_now=True)
	url = models.CharField(max_length=500)
	logo = models.ImageField(upload_to="static/logos", null=True)

	def __str__(self):
		return self.team_name
		
	def was_updated_recently(self):
		return self.updated_at >= timezone.now() - datetime.timedelta(days=30)
		
	def cache(self):
		if self.url and not self.logo:
			result = urllib.request.urlretrieve(self.url)
			self.logo.save(
					os.path.basename(self.url),
					File(open(result[0]))
					)
			self.save()

class Player(models.Model):
	first_name = models.CharField(max_length=200)
	last_name = models.CharField(max_length=200)
	team = models.ForeignKey(Team, on_delete=models.CASCADE)

	points = models.CharField(max_length=10)
	rebounds = models.CharField(max_length=10)
	assists = models.CharField(max_length=10)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.first_name + " " + self.last_name
		
	def was_updated_recently(self):
		return self.updated_at >= timezone.now() - datetime.timedelta(days=1)