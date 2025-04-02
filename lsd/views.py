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
import xlrd
from django.contrib import messages

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
        workbook = xlrd.open_workbook(file_contents=excel_file.read())
        sheet = workbook.sheet_by_index(0)
        
        # 验证必要的列是否存在
        headers = [str(sheet.cell_value(0, col)).strip() for col in range(sheet.ncols)]
        required_columns = ['序号', '姓名', '年龄', '职业', '群体选择', '电话', 
                          '是否有过性生活', '一年内是否做过宫颈癌筛查', 
                          '本次活动-HPV结果', '本次活动-TCT结果', '活检结果', '备注']
        
        missing_columns = [col for col in required_columns if col not in headers]
        if missing_columns:
            messages.error(request, f'Excel文件缺少必要的列: {", ".join(missing_columns)}')
            return redirect('lsd:survey_list')

        # 获取列索引
        column_indices = {col: headers.index(col) for col in required_columns}
        
        # 导入数据
        success_count = 0
        error_count = 0
        for row_idx in range(1, sheet.nrows):  # 从第二行开始（跳过表头）
            try:
                # 获取行数据
                row_data = {col: str(sheet.cell_value(row_idx, idx)).strip() for col, idx in column_indices.items()}
                
                # 转换布尔值
                sexual_experience = str(row_data['是否有过性生活']).lower() in ['是', '有', 'yes', 'true', '1']
                cervical_screening = str(row_data['一年内是否做过宫颈癌筛查']).lower() in ['是', '有', 'yes', 'true', '1']

                # 转换年龄为整数
                try:
                    age = int(float(row_data['年龄']))
                except (ValueError, TypeError):
                    age = 0

                # 转换手机号码为字符串
                phone = str(row_data['电话']).replace('.0', '')  # 处理Excel可能将数字加上.0的情况
                
                # 创建或更新调查记录
                survey, created = LsdSurvey.objects.update_or_create(
                    phone=phone,  # 使用手机号作为唯一标识
                    defaults={
                        '_openId': f"import_{phone}",
                        'name': row_data['姓名'],
                        'age': age,
                        'organization': organization,  # 使用当前用户的机构代码
                        'occupation': row_data['职业'],
                        'project': '蓝丝带公益行动',  # 默认项目名称
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
                logger.error(f'导入数据失败: {str(e)}, 行号: {row_idx + 1}, 数据: {row_data}')

        messages.success(request, f'成功导入 {success_count} 条数据，失败 {error_count} 条')
        return redirect('lsd:survey_list')

    except Exception as e:
        messages.error(request, f'导入失败: {str(e)}')
        return redirect('lsd:survey_list')
