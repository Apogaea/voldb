from django.db import models
from django.contrib.auth.models import User
from departments.models import Department

# Create your models here.
class Shift(models.Model):
	name = models.CharField(max_length=200)
	description = models.TextField()
	department = models.ForeignKey(Department, blank=True, null=True)
	start_time = models.DateTimeField('shift begins')
	end_time = models.DateTimeField('shift ends')
	owner = models.ForeignKey(User, blank=True, null=True, related_name='owner')
	def __str__(self):
		return self.name