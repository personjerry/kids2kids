from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import FormView
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
    # form = UserProfileForm(request.POST or None)
    # if request.method == 'POST' and form.is_valid():
    #     user = form.save()
    #     user_profile, created = UserProfile.objects.get_or_create(
    #         user=user, is_teacher=form.cleaned_data['is_teacher'])
    #     if created:
    #         messages.success(
    #             request, f'Account created for {user.username}!')
    #     else:
    #         messages.info(
    #             request, f'Account already exists for {user.username}!')
    #     return redirect('cohorts')
    # context = {'form': form}
    context = {}
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


@login_required
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

    # Add group to the context
    context['group'] = group

    # Use the actual URL pattern for joining a group
    # join_group_url = reverse("joingroup", args = [group.id])
    # context['join_group_url'] = join_group_url

    # Add group_id to the context
    context['group_id'] = group.id

    return render(request, 'cohorts.html', context)
