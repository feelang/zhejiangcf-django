# Generated by Django 3.2.8 on 2025-04-02 02:32

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LsdOrganization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='名称')),
                ('code', models.CharField(max_length=50, unique=True, verbose_name='代码')),
                ('remark', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='lsd.lsdorganization', verbose_name='父级机构')),
            ],
            options={
                'verbose_name': '组织机构',
                'verbose_name_plural': '组织机构',
                'db_table': 'lsd_organization',
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='LsdSurvey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_openId', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=50)),
                ('age', models.IntegerField()),
                ('phone', models.CharField(max_length=11, validators=[django.core.validators.RegexValidator(message='手机号码格式不正确', regex='^1[3-9]\\d{9}$')])),
                ('organization', models.CharField(max_length=100)),
                ('occupation', models.CharField(max_length=50)),
                ('project', models.CharField(max_length=100)),
                ('groupSelection', models.CharField(max_length=50)),
                ('sexualExperience', models.BooleanField()),
                ('cervicalCancerScreening', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('hpv_result', models.CharField(blank=True, choices=[('阴性', '阴性'), ('16型+', '16型+'), ('18/45型+', '18/45型+'), ('16型+ 18/45型+', '16型+ 18/45型+'), ('其余11型+', '其余11型+')], max_length=50, null=True)),
                ('tct_result', models.CharField(blank=True, choices=[('未做', '未做'), ('霉菌感染、滴虫感染', '霉菌感染、滴虫感染'), ('NILM', 'NILM'), ('ASC-US', 'ASC-US'), ('ASC-H', 'ASC-H'), ('LSIL', 'LSIL'), ('HSIL', 'HSIL'), ('AGC', 'AGC'), ('SCC', 'SCC')], max_length=50, null=True)),
                ('biopsy_result', models.TextField(blank=True, null=True)),
                ('remark', models.CharField(blank=True, max_length=500, null=True)),
            ],
            options={
                'verbose_name': '蓝丝带问卷调查表',
                'verbose_name_plural': '蓝丝带问卷调查表',
                'db_table': 'lsd_survey',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='lsd.lsdorganization', verbose_name='所属机构')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '用户资料',
                'verbose_name_plural': '用户资料',
                'db_table': 'lsd_user_profile',
            },
        ),
    ]
