from django.urls import path, include
from django.contrib import admin
from django.contrib.auth.views import LoginView
from wxcloudrun import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('admin/', admin.site.urls),
    path('survey/', include('lungsurvey.urls')),
]
