from rest_framework import serializers
from . import models

class ChoiceSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Choice
		fields = ('c_id', 'text', 'votes')


class QuestionSerializer(serializers.ModelSerializer):
	# many=True needed to allow RelatedManager to access all choices as a list
	choices = ChoiceSerializer(source='choice_set', many=True, read_only=True) 
	total_votes = serializers.SerializerMethodField()
	
	class Meta:
		model = models.Question
		fields = ('published_date', 'author', 'text', 'is_open', 'total_votes', 'choices', 'id')
		
	def get_total_votes(self, q):
		votes = 0
		choices = q.choice_set.all()
		for c in choices:
			votes += c.votes
		return votes
