from django.db import models
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from . import models
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserProfile, LearningGroup, UserProfileForm


User = get_user_model()

def index(request):
    return render(request, 'index.html')

class Login(FormView):
    form_class = AuthenticationForm
    success_url = reverse_lazy('index')
    template_name = 'login.html'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)
        login(self.request, user)


def register(request):
    # if request.method == 'POST':
    #     form = UserProfileForm(request.POST)
    #     if form.is_valid():
    #         user = form.save()
    #         user_profile, created = UserProfile.objects.get_or_create(
    #             user=user, is_teacher=form.cleaned_data['is_teacher'])
    #         if created:
    #             messages.success(
    #                 request, f'Account created for {user.username}!')
    #         else:
    #             messages.info(
    #                 request, f'Account already exists for {user.username}!')
    #         return redirect('cohorts')
    # else:
    #     form = UserProfileForm()
    return render(request, 'registration/signup.html', {'form': form})




def profile(request):
    return HttpResponse('hello, this is the profile')


@login_required
def join_group(request, group_id):
    group = get_object_or_404(LearningGroup, id=group_id)
    user_profile = request.user.userprofile
    if group in user_profile.learning_groups.all():
        return HttpResponse('You are already a member of this group.')
    else:
        user_profile.learning_groups.add(group)
        user_profile.save()
        messages.success(request, 'You have successfully joined the group.')
        return redirect('cohorts')


@login_required
def cohorts(request):
    cohorts = models.LearningGroup.objects.all()
    context = {'learning_groups': cohorts}
    group = cohorts.first()

    if request.method == 'POST':
        group_id = request.POST.get('group_id')
        user_profile = request.user.userprofile

        # Check if user is already a member of the group
        if user_profile.learning_groups.filter(id=group_id).exists():
            return HttpResponse('You are already a member of this group.')

        # Otherwise, add user to the group and save the user profile
        group = get_object_or_404(models.LearningGroup, id=group_id)
        user_profile.learning_groups.add(group)
        user_profile.save()
        return HttpResponse('You have successfully joined the group.')

    # Add group to the context
    context['group'] = group

    # Use the actual URL pattern for joining a group
    # join_group_url = reverse("joingroup", args = [group.id])
    # context['join_group_url'] = join_group_url


    # Add group_id to the context
    context['group_id'] = group.id

    return render(request, 'cohorts.html', context)






