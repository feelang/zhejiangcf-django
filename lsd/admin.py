from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import LsdOrganization, LsdSurvey, UserProfile

# 定义 UserProfile 的内联管理
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profile'

# 扩展 User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

# 重新注册 User 模型
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# 自定义LsdOrganization的管理界面
class LsdOrganizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'remark']

# 注册其他模型
admin.site.register(LsdOrganization, LsdOrganizationAdmin)
admin.site.register(LsdSurvey)
