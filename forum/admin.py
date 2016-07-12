from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(UserProfile)
admin.site.register(Topic)
admin.site.register(Thread)
admin.site.register(Message)
