from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class LsdOrganization(models.Model):
    name = models.CharField(max_length=100, verbose_name='Name')
    code = models.CharField(max_length=50, unique=True, verbose_name='Code')
    remark = models.TextField(blank=True, null=True, verbose_name='Remark')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name='Parent')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created Time')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated Time')

    class Meta:
        db_table = 'lsd_organization'
        verbose_name = 'LSD Organization'
        verbose_name_plural = 'LSD Organizations'
        ordering = ['name']

    def __str__(self):
        return self.name

# 用户资料模型，关联 User 和 LsdOrganization
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='用户')
    organization = models.ForeignKey(LsdOrganization, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='所属机构')
    
    class Meta:
        db_table = 'lsd_user_profile'
        verbose_name = 'User Profile'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

# 当创建用户时自动创建对应的 profile
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        if hasattr(instance, 'profile'):
            instance.profile.save()
    except UserProfile.DoesNotExist:
        pass  # 如果 profile 不存在，忽略

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
    # 群体选择
    GROUP_CHOICES = [
        ('低收入人群', '低收入人群'),
        ('失独家庭', '失独家庭'),
        ('残疾人群', '残疾人群'),
        ('困难家庭（低保、低编）', '困难家庭（低保、低编）'),
        ('援助证', '援助证'),
        ('都不是', '都不是'),
    ]
    groupSelection = models.CharField(max_length=50, choices=GROUP_CHOICES)
    # 性经历
    sexualExperience = models.BooleanField()
    # 宫颈癌筛查
    cervicalCancerScreening = models.BooleanField()
    # 创建时间
    created_at = models.DateTimeField(auto_now_add=True)
    # 更新时间
    updated_at = models.DateTimeField(auto_now=True)
    # HPV结果
    HPV_RESULT_CHOICES = [
        ('阴性', '阴性'),
        ('16型+', '16型+'),
        ('18/45型+', '18/45型+'),
        ('16型+ 18/45型+', '16型+ 18/45型+'),
        ('其余11型+', '其余11型+'),
    ]
    hpv_result = models.CharField(max_length=50, choices=HPV_RESULT_CHOICES, null=True, blank=True)
    # TCT结果
    TCT_RESULT_CHOICES = [
        ('未做', '未做'),
        ('霉菌感染、滴虫感染', '霉菌感染、滴虫感染'),
        ('NILM', 'NILM'),
        ('ASC-US', 'ASC-US'),
        ('ASC-H', 'ASC-H'),
        ('LSIL', 'LSIL'),
        ('HSIL', 'HSIL'),
        ('AGC', 'AGC'),
        ('SCC', 'SCC'),
    ]
    tct_result = models.CharField(max_length=50, choices=TCT_RESULT_CHOICES, null=True, blank=True)
    # 活检结果
    biopsy_result = models.TextField(null=True, blank=True)
    # 备注
    remark = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        db_table = 'lsd_survey'
        verbose_name = 'LSD Surveys'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.name} - {self.phone}'
