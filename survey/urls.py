from django.urls import path
from . import views

app_name = 'survey'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('submit/', views.submit_survey, name='submit_survey'),
    path('list/', views.get_surveys, name='get_surveys'),
]