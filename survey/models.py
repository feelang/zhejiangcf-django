from django.db import models
from django.core.validators import RegexValidator

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

    class Meta:
        db_table = 'lsd_survey'
        verbose_name = '蓝丝带问卷调查表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.name} - {self.phone}'
