from django.db import models

# "Add Group" -> dropdown of langauges -> dropdown of groups "Don't worry you can add more later"

class Language(models.Model):
    name = models.CharField(max_length=200)


class LearningGroup(models.Model):
    name = models.CharField(max_length=200)
    language = models.ForeignKey(Language, on_delete=models.DO_NOTHING)


class UserProfile(models.Model):
    is_teacher = models.BooleanField()
    learning_groups = models.ManyToManyField(LearningGroup)


class Lesson(models.Model):
    time = models.DateTimeField()
    description = models.CharField(max_length=200)
    teacher = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING, null=True, blank=False)
    learning_group = models.ForeignKey(LearningGroup, on_delete=models.DO_NOTHING)
