from django.urls import path
from . import views

urlpatterns = [
    path(r'activities/', views.ActivityList.as_view())
]
