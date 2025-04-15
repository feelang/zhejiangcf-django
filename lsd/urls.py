from django.urls import path
from . import views

app_name = 'lsd'

urlpatterns = [
    # 管理后台页面
    path('', views.index, name='index'),
    path('surveys/', views.survey_list, name='survey_list'),
    path('surveys/create/', views.create_survey_page, name='create_survey_page'),
    path('surveys/<int:survey_id>/edit/', views.edit_survey_page, name='edit_survey_page'),
    path('surveys/import/', views.import_surveys, name='import_surveys'),
    path('surveys/<int:survey_id>/update/', views.update_survey, name='update_survey'),
    path('surveys/<int:survey_id>/delete/', views.delete_survey, name='delete_survey'),
    path('statistics/', views.statistics, name='statistics'),
    path('export/', views.export_surveys, name='export_surveys'),
    path('download-template/', views.download_template, name='download_template'),

    # 管理后台API
    path('api/surveys/create/', views.create_survey, name='create_survey'),
    path('api/surveys/<int:survey_id>/update/', views.update_survey, name='update_survey'),
    path('api/surveys/<int:survey_id>/delete/', views.delete_survey, name='delete_survey'),

    # 微信小程序API
    path('api/weapp/surveys/', views.list_surveys_weapp, name='list_surveys_weapp'),
    path('api/weapp/surveys/create/', views.create_survey_weapp, name='create_survey_weapp'),
]