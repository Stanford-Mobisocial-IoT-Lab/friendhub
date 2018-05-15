from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from polls.models import Question, Choice
import datetime
import json

encoding = 'utf8'

############### Helpers ###############

# Check validity of request type and presence of arguments that are expcted
# Return (valid, data_or_response)
def validate_request(request, method, expected_fields):
	if request.method != method:
		return (False, JsonResponse({'success': False,
									 'info': 'must use %s request, used %s' % (method, request.method)}))
	if request.method not in ('POST', 'GET'):
		return (False, JsonResponse({'success': False,
									 'info': 'must use POST or GET request, used %s' % (request.method)}))
	
	data = (json.loads(request.body.decode(encoding)) if method == 'POST' else request.GET)

	missing = [fieldname for fieldname in expected_fields if fieldname not in data]
	if missing:
		return (False, JsonResponse({'success': False,
									 'info': 'request missing required arguments: '\
									 + ', '.join(missing)})) 

	return (True, data)



# Ensure that the question id matches an open question in the database.
# Return (valid, question_or_response), where question_or_response is a Question object
# if exactly one question matches the query, otherwise a JsonResponse indicating failure
def validate_qid_query(question_id, allow_closed=False):
	try: 
		q = Question.objects.get(id=question_id)
	except Question.DoesNotExist:
		return (False, JsonResponse({'success': False,
									 'info': 'No poll with id %s' % question_id}))
	if not allow_closed and not q.question_open:
		return (False, JsonResponse({'success': False,
									 'info': 'Poll %s is closed' % question_id}))

	return (True, q)


# Fetch a poll's results and optionally close it.
# If request successful, return JsonResponse with results of poll
# If request unsuccessful, return JsonResponse with reason for failure
def results_close_helper(request, close_poll=False):
	valid, data = validate_request(request, 'GET', ['question_id'])
	if not valid:
		return data

	valid, q_or_response = validate_qid_query(data.get('question_id'), allow_closed=True)
	if not valid:
		return q_or_response

	# Retrieve results
	q = q_or_response
	results = []
	for c in q.choice_set.all():
		results.append({'choice_id': c.choice_id,
						'choice_text': c.choice_text,
						'votes': c.votes})

	# Close poll if requested
	if close_poll:
		q.question_open = False
		q.save()
		
	return JsonResponse({'success': True,
						 'date': q.date,
						 'author': q.author,
						 'question': q.question_text,
						 'total_votes': q.get_total_votes(),
						 'open': q.question_open,
						 'results': results,
						 'info': ''})


############### Views ###############

# Return a list of polls
def poll_list(request):
	results = []	
	for q in Question.objects.all().order_by('-published_date'):
		results.append({'id': q.id,
						'question': q.question_text,
						'total_votes': q.get_total_votes()})
	return JsonResponse({'success': True,
						 'results': results})


# Create a poll via HTTP POST
# Expect JSON {question, author, choices}.
# Return JSON indicating success or failure
@csrf_exempt
def create(request):
	valid, data = validate_request(request, 'POST', ['question'])
	if not valid:
		return data	

	# Valid input; process
	qtext = str(data.get('question'))
	author = str(data.get('author', 'anonymous'))

	# Create question and choices for question
	q = Question.create(qtext, author)
	q.save()
	choices = [str(c) for c in data.get('choices', [])]
	for ctext in choices:
		c = Choice.create(ctext, q)
		c.save()

	return JsonResponse({'success': True, 'info': '', 'question_id': q.id})	

	
# Add choice to poll via HTTP POST
# Return JSON indicating success or failure
# Expect JSON {question_id, choice|choices}. choices overrides choice.
@csrf_exempt
def add_choice(request):
	valid, data = validate_request(request, 'POST', ['question_id'])
	if not valid:
		return data
	
	valid, q_or_response = validate_qid_query(data.get('question_id'))
	if not valid: # q_or_response is JsonResponse indicating failure; return
		return q_or_response

	# Add all choices that are not duplicates of existing ones. Report duplicates.
	q = q_or_response
	existing_choices = q.choice_set.all()
	duplicate_ctexts = []
	
	if 'choices' in data:
		choices = [str(c) for c in data.get('choices')]
	elif 'choice' in data:
		choices = [str(data.get('choice'))]
	else:
		choices = []

	for ctext in choices:
		if len(existing_choices.filter(choice_text=ctext)) > 0:
			duplicate_ctexts.append(ctext)
		else:
			c = Choice.create(ctext, q)
			c.save()

	# Return results
	info = ''
	if duplicate_ctexts:
		info = 'Duplicate choice(s) %s not added' % (', '.join(['"%s"' % ctext for ctext in duplicate_ctexts]))
		
	return JsonResponse({'success': True,
						 'info': info})
		

# Vote on poll via HTTP POST
# Return JSON indicating success or failure
# Expect JSON {question_id, choice_id}. Exactly one choice allowed
# TODO: In future support polls that allow selection of multiple choices?
# TODO: How would this handle a poll available to mutliple Almond users?
#       Would need to ensure that a user can only vote on a poll once or edit their response.
#       Difficult for a TV running only one Almond, however
@csrf_exempt
def vote(request):
	valid, data = validate_request(request, 'POST', ['question_id', 'choice_id'])
	if not valid:
		return data

	valid, q_or_response = validate_qid_query(data.get('question_id'))
	if not valid: # return failure
		return q_or_response
	
	# Ensure there is exactly one choice being voted on
	cid = data.get('choice_id')
	if cid is None:
		return JsonResponse({'success': False,
							 'info': 'Must select a choice to vote for'})
		
	# Vote on choice if exists.
	q = q_or_response
	try:
		c = q.choice_set.get(choice_id=cid)
		c.votes += 1
		c.save()
		info = 'Choice %s ("%s") now has %s votes.' % (cid, c.choice_text, c.votes)
	except Choice.DoesNotExist:
		return JsonResponse({'success': False,
							 'info': 'Choice %s does not exist.' % cid})
		
		c = Choice.create(ctext, q)
		c.votes = 1
		c.save()
		info = 'Choice "%s" did not exist; created it.' % ctext

	return JsonResponse({'success': True,
						 'info': info})	


# See results of poll via HTTP GET
# Return JSON with success or failure, and results with title and
# list of choices if success.
# Expect JSON {question_id}
def results(request):
	return results_close_helper(request)

# Close poll via HTTP GET
# If poll exists, show results
# Expect JSON {question_id}
def close(request):
	return results_close_helper(request, close_poll=True)


# Delete poll via HTTP POST
# Expect JSON {question_id}
@csrf_exempt
def delete(request):
	valid, data = validate_request(request, 'POST', ['question_id'])
	if not valid:
		return data

	# Valid request; process
	valid, q_or_response = validate_qid_query(data.get('question_id'), allow_closed=True)
	if not valid:
		return q_or_response

	# Delete the question
	q = q_or_response
	q.delete()

	return JsonResponse({'success': True,
						 'info': ''})
