from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
	url(r'^$', views.PollList.as_view()),
	url(r'^(?P<poll_id>[0-9]+)/$', views.poll_results),
	url(r'^(?P<poll_id>[0-9]+)/add_choice/$', views.add_choice),
	url(r'^(?P<poll_id>[0-9]+)/close/$', views.close),
	url(r'^(?P<poll_id>[0-9]+)/delete/$', views.delete),
	url(r'^(?P<poll_id>[0-9]+)/(?P<choice_id>[0-9]+)/$', views.vote),
]
