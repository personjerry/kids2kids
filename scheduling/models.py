from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django import forms

class Language(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class LearningGroup(models.Model):
    name = models.CharField(max_length=200)
    language = models.ForeignKey(Language, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    is_teacher = models.BooleanField(default=False)
    learning_groups = models.ManyToManyField(LearningGroup)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class UserProfileForm(UserCreationForm):
    is_teacher = forms.BooleanField(required=False, widget=forms.CheckboxInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        user_profile = UserProfile(
            user=user, is_teacher=self.cleaned_data['is_teacher'])
        user_profile.save()
        return user, user_profile

class Lesson(models.Model):
    time = models.DateTimeField()
    description = models.CharField(max_length=200)
    teacher = models.ForeignKey(
        UserProfile, on_delete=models.DO_NOTHING, null=True, blank=False)
    learning_group = models.ForeignKey(
        LearningGroup, on_delete=models.DO_NOTHING)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    from scheduling.models import UserProfile  # move import statement here
    if created:
        UserProfile.objects.create(user=instance)
