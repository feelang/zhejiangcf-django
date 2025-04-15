from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from django.core.serializers import serialize

@login_required
def index(request):
    try:
        organization = request.user.profile.organization.name if hasattr(request.user, 'profile') and request.user.profile.organization else "未设置"
    except:
        organization = "未设置"
        
    context = {
        'username': request.user.username,
        'organization': organization
    }
    return render(request, 'lungsurvey/index.html', context)