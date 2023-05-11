from django.contrib import admin

from .models import LearningGroup, Language, UserProfile, Lesson

admin.site.register(LearningGroup)
admin.site.register(Language)
admin.site.register(UserProfile)
admin.site.register(Lesson)
