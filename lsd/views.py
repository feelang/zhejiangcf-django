import logging
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import LsdSurvey
from django.core.serializers import serialize
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

logger = logging.getLogger('log')

@csrf_exempt
@require_http_methods(["POST"])
def submit_survey(request):
    try:
        data = json.loads(request.body)

        # 从请求头获取微信云托管注入的openid
        openid = request.headers.get('X-WX-OPENID') or request.headers.get('X-WX-FROM-OPENID')
        logger.info(f'openid: {openid}')  # Add this line for debuggin
        if not openid:
            return JsonResponse({
                'code': 401,
                'message': '未授权访问'
            }, status=401)

        # 创建新的调查记录
        survey = LsdSurvey(
            _openId=openid,
            name=data.get('name'),
            age=data.get('age'),
            phone=data.get('phone'),
            organization=data.get('organization'),
            occupation=data.get('occupation'),
            project=data.get('project'),
            groupSelection=data.get('groupSelection'),
            sexualExperience=data.get('sexualExperience'),
            cervicalCancerScreening=data.get('cervicalCancerScreening')
        )

        # 保存到数据库
        survey.save()

        return JsonResponse({
            'code': 0,
            'message': '提交成功',
            'data': {
                'id': survey.id
            }
        })
    except json.JSONDecodeError:
        return JsonResponse({
            'code': 400,
            'message': '无效的JSON数据'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'code': 500,
            'message': str(e)
        }, status=500)

@require_http_methods(["GET"])
def get_surveys(request):
    try:
        # 从请求头获取微信云托管注入的openid
        openId = request.headers.get('X-WX-OPENID') or request.headers.get('X-WX-FROM-OPENID')
        logger.info(f'openId: {openId}')  # Add this line for debuggin
        if not openId:
            return JsonResponse({
                'code': 401,
                'message': '未授权访问'
            }, status=401)

        # 查询该用户的所有问卷
        surveys = LsdSurvey.objects.filter(_openId=openId).values(
            'id', '_openId', 'name', 'age', 'phone', 'organization',
            'occupation', 'project', 'groupSelection',
            'sexualExperience', 'cervicalCancerScreening',
            'created_at', 'updated_at'
        )

        return JsonResponse({
            'code': 0,
            'message': '查询成功',
            'data': list(surveys)
        })
    except Exception as e:
        return JsonResponse({
            'code': 500,
            'message': str(e)
        }, status=500)


@login_required
@require_http_methods(["POST"])
def update_survey(request, survey_id):
    try:
        data = json.loads(request.body)
        survey = LsdSurvey.objects.get(id=survey_id)
        
        # 更新问卷数据
        if data.get('name') is not None:
            survey.name = data.get('name')
        if data.get('age') is not None:
            survey.age = data.get('age')
        if data.get('phone') is not None:
            survey.phone = data.get('phone')
        if data.get('organization') is not None:
            survey.organization = data.get('organization')
        if data.get('occupation') is not None:
            survey.occupation = data.get('occupation')
        if data.get('project') is not None:
            survey.project = data.get('project')
        if data.get('groupSelection') is not None:
            survey.groupSelection = data.get('groupSelection')
        if data.get('sexualExperience') is not None:
            survey.sexualExperience = data.get('sexualExperience')
        if data.get('cervicalCancerScreening') is not None:
            survey.cervicalCancerScreening = data.get('cervicalCancerScreening')
        if data.get('hpv_result') is not None:
            survey.hpv_result = data.get('hpv_result')
        if data.get('tct_result') is not None:
            survey.tct_result = data.get('tct_result')
        if data.get('biopsy_result') is not None:
            survey.biopsy_result = data.get('biopsy_result')
        if data.get('remark') is not None:
            survey.remark = data.get('remark')
        survey.save()
        
        return JsonResponse({
            'code': 0,
            'message': '更新成功'
        })
    except LsdSurvey.DoesNotExist:
        return JsonResponse({
            'code': 404,
            'message': '问卷不存在'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'code': 500,
            'message': str(e)
        }, status=500)

@login_required
@require_http_methods(["GET"])
def survey_list(request):
    try:
        # 获取搜索参数
        search_query = request.GET.get('search', '')
        
        # 创建基础查询
        survey_list = LsdSurvey.objects.order_by('-created_at')
        
        # 如果有搜索关键词，添加搜索条件
        if search_query:
            from django.db.models import Q
            survey_list = survey_list.filter(
                Q(name__icontains=search_query) |
                Q(phone__icontains=search_query)
            )
        
        # 设置每页显示10条记录
        paginator = Paginator(survey_list, 10)
        
        # 获取页码参数，默认为第1页
        page = request.GET.get('page', 1)
        try:
            surveys = paginator.page(page)
        except PageNotAnInteger:
            surveys = paginator.page(1)
        except EmptyPage:
            surveys = paginator.page(paginator.num_pages)

        return render(request, 'lsd/survey_list.html', {
            'surveys': surveys,
            'page_obj': surveys,
            'is_paginated': True
        })
    except Exception as e:
        return JsonResponse({
            'code': 500,
            'message': str(e)
        }, status=500)
