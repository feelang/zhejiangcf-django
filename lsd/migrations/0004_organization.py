from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('lsd', '0003_auto_20250327_0825'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='名称')),
                ('code', models.CharField(max_length=50, unique=True, verbose_name='代码')),
                ('remark', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=models.CASCADE, related_name='children', to='lsd.organization', verbose_name='父级机构')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '组织机构',
                'verbose_name_plural': '组织机构',
                'db_table': 'lsd_organization',
                'ordering': ['code'],
            },
        ),
    ]