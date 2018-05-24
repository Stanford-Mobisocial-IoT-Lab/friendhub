from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from polls.models import Question, Choice
from polls.serializer import QuestionSerializer, ChoiceSerializer


class PollList(APIView):
	# View the list of polls.
	def get(self, request):
		questions = Question.objects.all()
		serializer = QuestionSerializer(questions, many=True)
		return Response(serializer.data)

	# Add a poll to the list of polls.
	def post(self, request):
		data = request.data
		if 'question' not in data:
			return Response({'info': 'expected field question'}, status=status.HTTP_400_BAD_REQUEST)

		# Valid input; process it
		qtext = data.get('question')
		author = data.get('author', 'anonymous')
		q = Question.create(qtext, author)
		q.save()
		serializer = QuestionSerializer(q)
		return Response(serializer.data, status=status.HTTP_201_CREATED)

	
# View results for the given question.
@api_view(['GET'])
def poll_results(request, poll_id):
	# Use serializer to show results
	try:
		q = Question.objects.get(id=poll_id)
		serializer = QuestionSerializer(q)
		return Response(serializer.data)
	except Question.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	
# Add a choice to the provided question.
@api_view(['POST'])
def add_choice(request, poll_id):
	data = request.data
	if 'choice' not in data:
		return Response({'info': 'expected field choice'}, status=status.HTTP_400_BAD_REQUEST)
	
	try:
		q = Question.objects.get(id=poll_id)
		# Add choice with given text to poll
		ctext = data.get('choice')
		c = Choice.create(ctext, q)
		c.save()
		serializer = ChoiceSerializer(c)
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	except Question.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)		



# Close the provided question.
@api_view(['POST'])
def close(request, poll_id):
	try:
		q = Question.objects.get(id=poll_id)
		# Disable is_open flag
		q.is_open = False
		q.save()
		serializer = QuestionSerializer(q)
		return Response(serializer.data)
	except Question.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)



# Delete the provided question.
@api_view(['POST'])
def delete(request, poll_id):
	try:
		q = Question.objects.get(id=poll_id)
		q.delete()
		return Response({'info': 'successfully deleted poll %s' % poll_id})

	except Question.DoesNotExist:
		return Repsonse(status=status.HTTP_404_NOT_FOUND)


# Vote for the given choice on the given question.
@api_view(['POST'])
def vote(request, poll_id, choice_id):
	try:
		q = Question.objects.get(id=poll_id)
		c = q.choice_set.get(c_id=choice_id)
		c.votes += 1
		c.save()
		serializer = ChoiceSerializer(c)
		return Response(serializer.data)
	except Question.DoesNotExist:
		return Response({'info': 'no such question'}, status=status.HTTP_404_NOT_FOUND)
	except Choice.DoesNotExist:
		return Response({'info': 'no such choice'}, status=status.HTTP_404_NOT_FOUND)
