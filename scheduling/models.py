from django.db import models

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
    is_teacher = models.BooleanField()
    learning_groups = models.ManyToManyField(LearningGroup)


class Lesson(models.Model):
    time = models.DateTimeField()
    description = models.CharField(max_length=200)
    teacher = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING, null=True, blank=False)
    learning_group = models.ForeignKey(LearningGroup, on_delete=models.DO_NOTHING)
