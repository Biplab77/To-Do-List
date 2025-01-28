from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ToDoItem(models.Model):
	task_name = models.CharField(max_length=50)
	description = models.CharField(max_length=200)
	status = models.CharField(max_length=50, default="pending")
	date_created = models.DateTimeField('date created')
	user = models.ForeignKey(User, on_delete=models.CASCADE, default="")

class ToDoEvent(models.Model):
	event_name = models.CharField(max_length=50)
	description = models.CharField(max_length=200)
	status = models.CharField(max_length=50, default="pending")
	event_date = models.DateTimeField('event date')
	user = models.ForeignKey(User, on_delete=models.CASCADE, default="")
	