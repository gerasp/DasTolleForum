from django import template
from forum.models import UserProfile
register = template.Library()

@register.simple_tag
def profile_photo(request):
    return UserProfile.objects.get(user=request.user).photo.url