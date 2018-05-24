from django.db import models
import datetime

# Create your models here.
class Question(models.Model):
	def __str__(self):
		return self.text

	@classmethod
	def create(cls, qtext, author, pubdate=None):
		if pubdate is None:
			pubdate = datetime.datetime.now()
		return cls(text=qtext, author=author, published_date=pubdate)
	
	text = models.CharField(max_length=500)
	author = models.CharField(max_length=50, default='anonymous')
	published_date = models.DateTimeField('date published')
	is_open = models.BooleanField(default=True)
	max_choice_id = models.PositiveIntegerField(default=0)


class Choice(models.Model):
	def __str__(self):
		return self.text

	@classmethod
	def create(cls, ctext, question):
		question.max_choice_id += 1
		question.save()
		return cls(text=ctext, question=question, c_id=question.max_choice_id)

	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	text = models.CharField(max_length=100)
	c_id = models.PositiveIntegerField(default=0)
	votes = models.IntegerField(default=0)
	
