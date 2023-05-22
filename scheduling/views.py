from django import forms
from .models import UserProfile
from .models import CustomUserCreationForm
from django.contrib.auth import get_user_model, login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .models import *

User = get_user_model()


def index(request):
    return render(request, 'index.html')


class Login(FormView):
    form_class = AuthenticationForm
    success_url = reverse_lazy('index')
    # template_name = 'login.html'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)
        login(self.request, user)


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'email': form.cleaned_data['email'],
                    'is_teacher': form.cleaned_data['is_teacher']
                }
            )
            if created:
                messages.success(
                    request, f'Account created for {user.username}!')
            else:
                messages.info(
                    request, f'Account already exists for {user.username}!')

            # Log in the user
            login(request, user)

            return redirect('scheduling:cohorts')
    else:
        form = CustomUserCreationForm()

    context = {'form': form}
    return render(request, 'registration/signup.html', context)


@login_required
def profile(request):
    return render(request, 'profile.html')


@login_required
def join_group(request, group_id):
    group = get_object_or_404(LearningGroup, id=group_id)
    user_profile = request.user.userprofile
    if group in user_profile.learning_groups.all():
        messages.warning(request, 'You are already a member of this group.')
    else:
        user_profile.learning_groups.add(group)
        user_profile.save()
        messages.success(request, 'You have successfully joined the group.')
    return redirect('cohorts')


def cohorts(request):
    cohorts = LearningGroup.objects.all()
    context = {'learning_groups': cohorts}
    group = cohorts.first()

    if request.method == 'POST':
        group_id = request.POST.get('group_id')
        user_profile = request.user.userprofile

        # Check if user is already a member of the group
        if user_profile.learning_groups.filter(id=group_id).exists():
            messages.warning(
                request, 'You are already a member of this group.')
        else:
            # Otherwise, add user to the group and save the user profile
            group = get_object_or_404(LearningGroup, id=group_id)
            user_profile.learning_groups.add(group)
            user_profile.save()
            messages.success(
                request, 'You have successfully joined the group.')

    context['group'] = group
    context['group_id'] = group.id

    return render(request, 'cohorts.html', context)
