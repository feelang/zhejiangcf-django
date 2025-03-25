from django.urls import path, include
from django.contrib import admin
from wxcloudrun import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/count/', views.counter),
    path('api/count', views.counter),
    path('survey/', include('survey.urls')),
]
