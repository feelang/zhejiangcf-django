from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

app_name = 'survey'

urlpatterns = [
    path('', views.index, name='index'),
]