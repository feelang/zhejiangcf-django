from django.urls import path
from . import views

app_name = 'lsd'

urlpatterns = [
    path('submit/', views.submit_survey, name='submit_survey'),
    path('list/', views.get_surveys, name='get_surveys'),
    path('survey-list/', views.survey_list, name='survey_list'),
]