import logging
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import LsdOrganization, LsdSurvey

logger = logging.getLogger('log')

@csrf_exempt
@require_http_methods(["POST"])
def create_survey(request):
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

        # 群体选择列表
        GROUP_SELECTION_LIST = ['低收入人群', '失独家庭', '残疾人群', '困难家庭（低保、低编）', '援助证', '都不是']
        
        # 验证 groupSelection 是否为有效的数组下标
        group_selection_index = data.get('groupSelection')
        try:
            group_selection_index = int(group_selection_index)
        except (ValueError, TypeError):
            return JsonResponse({
                'code': 400,
                'message': '无效的群体选择'
            }, status=400)
            
        if group_selection_index < 0 or group_selection_index >= len(GROUP_SELECTION_LIST):
            return JsonResponse({
                'code': 400,
                'message': '无效的群体选择'
            }, status=400)

        # 验证 sexualExperience 和 cervicalCancerScreening 是否为 0 或 1
        sexual_experience = data.get('sexualExperience')
        cervical_screening = data.get('cervicalCancerScreening')
        try:
            sexual_experience = int(sexual_experience)
            cervical_screening = int(cervical_screening)
        except (ValueError, TypeError):
            return JsonResponse({
                'code': 400,
                'message': 'sexualExperience 和 cervicalCancerScreening 必须为 0 或 1'
            }, status=400)
        if sexual_experience not in [0, 1] or cervical_screening not in [0, 1]:
            return JsonResponse({
                'code': 400,
                'message': 'sexualExperience 和 cervicalCancerScreening 必须为 0 或 1'
            }, status=400)

        # 创建新的调查记录
        survey = LsdSurvey(
            _openId=openid,
            name=data.get('name'),
            age=data.get('age'),
            phone=data.get('phone'),
            organization=data.get('organization'),
            occupation=data.get('occupation'),
            project=data.get('project'),
            groupSelection=GROUP_SELECTION_LIST[group_selection_index],
            sexualExperience=bool(sexual_experience),
            cervicalCancerScreening=bool(cervical_screening)
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
def list_surveys(request):
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

@require_http_methods(["GET"])
def list_organizations(request):
    try:
        # 从请求头获取微信云托管注入的openid
        openId = request.headers.get('X-WX-OPENID') or request.headers.get('X-WX-FROM-OPENID')
        if not openId:
            return JsonResponse({
                'code': 401,
                'message': '未授权访问'
            }, status=401)

        # 查询所有的组织名称
        organizations = LsdOrganization.objects.all()
        return JsonResponse({
            'code': 0,
            'message': '查询成功',
            'data': [{"name": org.name, "code": org.code} for org in organizations],
        }, status=200)
    except Exception as e:
        return JsonResponse({
            'code': 500,
            'message': str(e)
        }, status=500)