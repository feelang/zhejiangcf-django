import json
import logging

from django.http import JsonResponse
from django.shortcuts import render
from wxcloudrun.models import Counters
from django.contrib.auth.decorators import login_required


logger = logging.getLogger('log')

@login_required
def index(request, _):
    """
    获取主页

     `` request `` 请求对象
    """

    return render(request, 'index.html')