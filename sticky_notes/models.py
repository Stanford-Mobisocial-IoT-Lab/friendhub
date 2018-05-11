from django.db import models

# Create your models here.

class Post(models.Model):
    author = models.CharField(max_length=50)
    post = models.TextField()
    date = models.DateTimeField(auto_now=True)

