from forum.models import UserProfile

def profile_photo(request):
    return {
        'profile_photo': UserProfile.objects.get(user=request.user).photo.url
    }