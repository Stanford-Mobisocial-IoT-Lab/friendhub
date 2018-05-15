from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
	url(r'^$', views.poll_list, name='poll_list'),
	url(r'^create/$', views.create, name='create'),
	url(r'^add_choice/$', views.add_choice, name='add_choice'),
	url(r'^vote/$', views.vote, name='vote'),
	url(r'^results/$', views.results, name='results'),
	url(r'^close/$', views.close, name='close'),
	url(r'^delete/$', views.delete, name='delete'),
]
