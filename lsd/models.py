from django.db import models
from django.core.validators import RegexValidator

class LsdOrganization(models.Model):
    name = models.CharField(max_length=100, verbose_name='名称')
    code = models.CharField(max_length=50, unique=True, verbose_name='代码')
    remark = models.TextField(blank=True, null=True, verbose_name='备注')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name='父级机构')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'lsd_organization'
        verbose_name = '组织机构'
        verbose_name_plural = verbose_name
        ordering = ['code']

    def __str__(self):
        return self.name

# Create your models here.
class LsdSurvey(models.Model):
    # 用户唯一标识
    _openId = models.CharField(max_length=100)
    # 姓名
    name = models.CharField(max_length=50)
    # 年龄
    age = models.IntegerField()
    # 手机号码，使用正则验证
    phone_regex = RegexValidator(
        regex=r'^1[3-9]\d{9}$',
        message='手机号码格式不正确'
    )
    phone = models.CharField(validators=[phone_regex], max_length=11)
    # 单位
    organization = models.CharField(max_length=100)
    # 职业
    occupation = models.CharField(max_length=50)
    # 项目
    project = models.CharField(max_length=100)
    # 分组选择
    groupSelection = models.CharField(max_length=50)
    # 性经历
    sexualExperience = models.BooleanField()
    # 宫颈癌筛查
    cervicalCancerScreening = models.BooleanField()
    # 创建时间
    created_at = models.DateTimeField(auto_now_add=True)
    # 更新时间
    updated_at = models.DateTimeField(auto_now=True)
    # HPV结果
    hpv_result = models.SmallIntegerField(null=True, blank=True)
    # TCT结果
    tct_result = models.SmallIntegerField(null=True, blank=True)
    # 活检结果
    biopsy_result = models.SmallIntegerField(null=True, blank=True)
    # 备注
    remark = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        db_table = 'lsd_survey'
        verbose_name = '蓝丝带问卷调查表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.name} - {self.phone}'
