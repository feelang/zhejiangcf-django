from django.urls import path
from . import views

app_name = 'lsd'

urlpatterns = [
    path('', views.survey_list, name='survey_list'),
    path('submit/', views.submit_survey, name='submit_survey'),
    path('list/', views.get_surveys, name='get_surveys'),
    path('api/surveys/<int:survey_id>/update/', views.update_survey, name='update_survey'),
    path('import/', views.import_surveys, name='import_surveys'),
]