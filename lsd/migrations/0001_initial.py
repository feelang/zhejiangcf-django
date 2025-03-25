# Generated by Django 3.2.8 on 2025-03-25 14:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
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
            ],
            options={
                'verbose_name': '蓝丝带问卷调查表',
                'verbose_name_plural': '蓝丝带问卷调查表',
                'db_table': 'lsd_survey',
            },
        ),
    ]
