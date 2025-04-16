"""
Constants for the LSD application
"""

# Error messages
ERROR_NO_ORGANIZATION = '您未关联机构信息，请联系管理员进行关联'
ERROR_NO_PERMISSION = '您没有权限访问此页面'
ERROR_NO_PERMISSION_DELETE = '您没有权限删除此问卷'
ERROR_SURVEY_NOT_FOUND = '问卷不存在'
ERROR_INVALID_JSON = '无效的JSON数据'
ERROR_UNAUTHORIZED = '未授权访问'
ERROR_USER_NO_ORGANIZATION = '用户未关联机构信息'

# Success messages
SUCCESS_CREATE = '添加成功'
SUCCESS_UPDATE = '更新成功'
SUCCESS_DELETE = '删除成功'
SUCCESS_QUERY = '查询成功'

# File related messages
ERROR_NO_EXCEL_FILE = '请选择要导入的Excel文件'
ERROR_INVALID_EXCEL_FORMAT = '请上传Excel文件(.xls或.xlsx)'
ERROR_MISSING_COLUMNS = 'Excel文件缺少必要的列: {columns}'

# Survey related constants
REQUIRED_COLUMNS = [
    '姓名', '年龄', '职业', '群体选择', '电话', 
    '是否有过性生活', '一年内是否做过宫颈癌筛查', 
    '本次活动-HPV结果', '本次活动-TCT结果', '活检结果', '备注'
]

PROJECT_NAME = 'LSD2025' 