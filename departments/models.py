from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
	name = models.CharField(max_length=200)
	description = models.TextField()
	lead = models.ForeignKey(User, blank=True, null=True, related_name='lead')
	liaison = models.ForeignKey(User, blank=True, null=True, related_name='liason')
	def __str__(self):
		return self.name