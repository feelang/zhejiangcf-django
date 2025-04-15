from django.urls import path
from . import views

app_name = 'lsd'

urlpatterns = [
    # 管理后台页面
    path('', views.list_surveys, name='list_surveys'),
    path('create/', views.create_survey_page, name='create_survey_page'),
    path('import/', views.import_surveys, name='import_surveys'),

    # 管理后台API
    path('api/surveys/create/', views.create_survey, name='create_survey'),
    path('api/surveys/<int:survey_id>/update/', views.update_survey, name='update_survey'),
    path('api/surveys/<int:survey_id>/delete/', views.delete_survey, name='delete_survey'),

    # 微信小程序API
    path('api/weapp/surveys/', views.list_surveys_weapp, name='list_surveys_weapp'),
    path('api/weapp/surveys/create/', views.create_survey_weapp, name='create_survey_weapp'),
]