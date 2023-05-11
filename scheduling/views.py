from django.shortcuts import render
from django.http import HttpResponse

from . import models


def index(request):
    return render(request, 'index.html')

def login(request):
    return HttpResponse('hello, this is the login')

def register(request):
    return HttpResponse('hello, this is the register')

def profile(request):
    return HttpResponse('hello, this is the profile')

def cohorts(request):
    cohorts = models.LearningGroup.objects.all()
    return HttpResponse('<br>'.join(cohort.name for cohort in cohorts))
