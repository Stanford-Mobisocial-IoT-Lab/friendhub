from django.db import models
import datetime

# Create your models here.
class Question(models.Model):
	def __str__(self):
		return self.question_text

	@classmethod
	def create(cls, qtext, author, pubdate=None):
		if pubdate is None:
			pubdate = datetime.datetime.now()
		return cls(question_text=qtext, author=author, published_date=pubdate)

	def get_total_votes(self):
		votes = 0
		choices = self.choice_set.all()
		for c in choices:
			votes += c.votes
		return votes
	
	question_text = models.CharField(max_length=500)
	author = models.CharField(max_length=50, default='anonymous')
	published_date = models.DateTimeField('date published')
	question_open = models.BooleanField(default=True)
	max_choice_id = models.PositiveIntegerField(default=0)

	# TODO: Incorporate authentication when Silei has example ready


class Choice(models.Model):
	def __str__(self):
		return self.choice_text

	@classmethod
	def create(cls, ctext, question):
		question.max_choice_id += 1
		question.save()
		return cls(choice_text=ctext, question=question, choice_id = question.max_choice_id)

	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	choice_text = models.CharField(max_length=100)
	choice_id = models.PositiveIntegerField(default=0)
	votes = models.IntegerField(default=0)
	
