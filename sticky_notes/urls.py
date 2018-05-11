from django.urls import path
from . import views

urlpatterns = [
    path(r'posts/', views.PostList.as_view())
]
