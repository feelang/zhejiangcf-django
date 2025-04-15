from django.urls import path
from . import views
from . import weapp_views

app_name = 'lsd'

urlpatterns = [
    # 管理后台页面
    path('', views.index, name='index'),
    path('surveys/', views.survey_list, name='survey_list'),
    path('surveys/create/', views.create_survey_page, name='create_survey_page'),
    path('surveys/<int:survey_id>/edit/', views.edit_survey_page, name='edit_survey_page'),
    path('surveys/import/', views.import_surveys, name='import_surveys'),
    path('statistics/', views.statistics, name='statistics'),
    path('export/', views.export_surveys, name='export_surveys'),

    # 管理后台API
    path('api/surveys/create/', views.create_survey, name='create_survey'),
    path('api/surveys/<int:survey_id>/update/', views.update_survey, name='update_survey'),
    path('api/surveys/<int:survey_id>/delete/', views.delete_survey, name='delete_survey'),

    # 微信小程序API
    path('api/weapp/surveys/', weapp_views.list_surveys, name='list_surveys_weapp'),
    path('api/weapp/surveys/create/', weapp_views.create_survey, name='create_survey_weapp'),
]