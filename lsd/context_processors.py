from .models import UserProfile

def organization_info(request):
    if request.user.is_authenticated:
        try:
            user_profile = request.user.profile
            organization = user_profile.organization if user_profile and user_profile.organization else None
            return {
                'organization_name': organization.name if organization else None,
                'organization_code': organization.code if organization else None,
            }
        except UserProfile.DoesNotExist:
            return {
                'organization_name': None,
                'organization_code': None,
            }
    return {
        'organization_name': None,
        'organization_code': None,
    } 