from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django import forms



class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    is_teacher = forms.BooleanField(required=False, widget=forms.CheckboxInput)

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email', 'is_teacher')



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
    email = models.EmailField(default='default@example.com')
    learning_groups = models.ManyToManyField(LearningGroup)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=False, blank=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username



class Lesson(models.Model):
    time = models.DateTimeField()
    description = models.CharField(max_length=200)
    # set ForeignKey to use UserProfile model
    teacher = models.ForeignKey(
        UserProfile, on_delete=models.DO_NOTHING, null=True, blank=False)
    # set ForeignKey to use LearningGroup model
    learning_group = models.ForeignKey(
        LearningGroup, on_delete=models.DO_NOTHING)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    # import UserProfile model here instead of at the beginning to avoid circular import
    from scheduling.models import UserProfile
    if created:
        UserProfile.objects.create(user=instance)
