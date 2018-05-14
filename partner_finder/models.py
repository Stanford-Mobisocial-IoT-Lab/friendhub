from django.db import models

# Create your models here.

class Activity(models.Model):
    organizer = models.CharField(max_length=50)
    activity = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    post_time = models.DateTimeField(auto_now=True) # when post was made

