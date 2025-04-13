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
import openpyxl
from django.contrib import messages
from django.db.models import Q
from .models import UserProfile
import re

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
def survey_list(request):
    # 获取用户所属机构
    try:
        user_profile = request.user.profile
        organization = user_profile.organization if user_profile and user_profile.organization else None
        organization_code = organization.code if organization else None
        logger.info(f'organization_code: {organization_code}')
    except UserProfile.DoesNotExist:
        organization = None
        organization_code = None

    # 如果是staff用户，允许查看所有问卷
    if request.user.is_staff:
        organization = None
        organization_code = None
        logger.info('User is staff, showing all surveys')
    elif organization_code is None:
        messages.error(request, '用户未关联机构信息，请联系管理员进行关联')
        return render(request, 'lsd/survey_list.html', {
            'surveys': [],
            'search_query': '',
            'organization': None,
            'organization_code': None,
            'show_error_modal': True
        })

    # 获取搜索参数
    search_query = request.GET.get('search', '')
    
    # 构建查询
    surveys = LsdSurvey.objects.all()
    
    # 根据机构过滤
    if organization_code:
        surveys = surveys.filter(organization=organization_code)
    
    # 如果有搜索查询，添加搜索条件
    if search_query:
        surveys = surveys.filter(
            Q(name__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(hpv_result__icontains=search_query) |
            Q(tct_result__icontains=search_query)
        )
    
    # 按更新时间倒序排序
    surveys = surveys.order_by('-updated_at')
    
    # 分页
    page = request.GET.get('page', 1)
    paginator = Paginator(surveys, 10)  
    
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    return render(request, 'lsd/survey_list.html', {
        'surveys': page_obj,
        'search_query': search_query,
        'organization': organization,
        'organization_code': organization_code,
        'show_error_modal': False,
        'is_staff': request.user.is_staff,
        'is_paginated': paginator.num_pages > 1,
        'page_obj': page_obj
    })

@login_required
@require_http_methods(["POST"])
def import_surveys(request):
    try:
        if 'excel_file' not in request.FILES:
            messages.error(request, '请选择要导入的Excel文件')
            return redirect('lsd:survey_list')

        excel_file = request.FILES['excel_file']
        if not excel_file.name.endswith(('.xls', '.xlsx')):
            messages.error(request, '请上传Excel文件(.xls或.xlsx)')
            return redirect('lsd:survey_list')

        # 从用户 profile 获取机构信息
        organization = request.user.profile.organization.code if request.user.profile and request.user.profile.organization else ''
        if not organization:
            messages.error(request, '用户未关联机构信息')
            return redirect('lsd:survey_list')

        # 读取Excel文件
        workbook = openpyxl.load_workbook(excel_file)
        sheet = workbook.active
        
        # 验证必要的列是否存在
        headers = [str(cell.value).strip() for cell in sheet[1]]
        required_columns = ['序号', '姓名', '年龄', '职业', '群体选择', '电话', 
                          '是否有过性生活', '一年内是否做过宫颈癌筛查', 
                          '本次活动-HPV结果', '本次活动-TCT结果', '活检结果', '备注']
        
        missing_columns = [col for col in required_columns if col not in headers]
        if missing_columns:
            messages.error(request, f'Excel文件缺少必要的列: {", ".join(missing_columns)}')
            return redirect('lsd:survey_list')

        # 获取列索引
        column_indices = {col: headers.index(col) + 1 for col in required_columns}
        
        # 导入数据
        success_count = 0
        error_count = 0
        skipped_count = 0
        invalid_phone_count = 0
        invalid_phone_records = []
        
        for row_idx, row in enumerate(sheet.iter_rows(min_row=2), start=2):  # 从第二行开始（跳过表头）
            try:
                # 获取行数据
                row_data = {col: str(row[idx-1].value).strip() if row[idx-1].value is not None else '' for col, idx in column_indices.items()}
                
                # 检查姓名和电话是否为空
                if not row_data['姓名'] or not row_data['电话']:
                    skipped_count += 1
                    logger.info(f'跳过空数据行: 行号 {row_idx}, 姓名: {row_data["姓名"]}, 电话: {row_data["电话"]}')
                    continue
                
                # 处理并验证手机号
                phone = str(row_data['电话']).replace('.0', '')  # 处理Excel可能将数字加上.0的情况
                is_valid_phone = bool(re.match(r'^1[3-9]\d{9}$', phone))  # 验证中国大陆手机号格式
                
                if not is_valid_phone:
                    invalid_phone_count += 1
                    invalid_phone_records.append(f"行号 {row_idx}: {row_data['姓名']} ({phone})")
                    logger.info(f'无效手机号: 行号 {row_idx}, 姓名: {row_data["姓名"]}, 电话: {phone}')
                
                # 转换布尔值
                sexual_experience = str(row_data['是否有过性生活']).lower() in ['是', '有', 'yes', 'true', '1']
                cervical_screening = str(row_data['一年内是否做过宫颈癌筛查']).lower() in ['是', '有', 'yes', 'true', '1']

                # 转换年龄为整数
                try:
                    age = int(float(row_data['年龄']))
                except (ValueError, TypeError):
                    age = 0
                
                # 创建或更新调查记录
                survey, created = LsdSurvey.objects.update_or_create(
                    phone=phone,
                    name=row_data['姓名'],
                    defaults={
                        '_openId': f"import_{phone}",
                        'age': age,
                        'organization': organization,
                        'occupation': row_data['职业'],
                        'project': '蓝丝带公益行动',
                        'groupSelection': row_data['群体选择'],
                        'sexualExperience': sexual_experience,
                        'cervicalCancerScreening': cervical_screening,
                        'hpv_result': row_data['本次活动-HPV结果'],
                        'tct_result': row_data['本次活动-TCT结果'],
                        'biopsy_result': row_data['活检结果'],
                        'remark': row_data['备注']
                    }
                )
                
                success_count += 1
            except Exception as e:
                error_count += 1
                logger.error(f'导入数据失败: {str(e)}, 行号: {row_idx}, 数据: {row_data}')

        # 构建消息
        message = f'成功导入 {success_count} 条数据，失败 {error_count} 条，跳过 {skipped_count} 条空数据'
        if invalid_phone_count > 0:
            message += f'，其中 {invalid_phone_count} 条手机号格式不正确'
            if len(invalid_phone_records) <= 5:  # 如果无效手机号记录不多，直接显示
                message += f'：{", ".join(invalid_phone_records)}'
            else:  # 如果无效手机号记录较多，只显示前5条
                message += f'：{", ".join(invalid_phone_records[:5])}等'
        
        messages.success(request, message)
        return redirect('lsd:survey_list')

    except Exception as e:
        messages.error(request, f'导入失败: {str(e)}')
        return redirect('lsd:survey_list')

@login_required
@require_http_methods(["POST"])
def delete_survey(request, survey_id):
    try:
        survey = LsdSurvey.objects.get(id=survey_id)
        
        # 检查用户权限
        if not request.user.is_staff:
            # 获取用户所属机构
            try:
                user_profile = request.user.profile
                organization = user_profile.organization if user_profile and user_profile.organization else None
                organization_code = organization.code if organization else None
                
                # 如果用户不是staff且问卷不属于用户所在机构，则拒绝删除
                if organization_code != survey.organization:
                    return JsonResponse({
                        'code': 403,
                        'message': '您没有权限删除此问卷'
                    }, status=403)
            except UserProfile.DoesNotExist:
                return JsonResponse({
                    'code': 403,
                    'message': '您没有权限删除此问卷'
                }, status=403)
        
        # 删除问卷
        survey.delete()
        
        return JsonResponse({
            'code': 0,
            'message': '删除成功'
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
