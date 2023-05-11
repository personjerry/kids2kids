from django.urls import path

from . import views

app_name = 'scheduling'

urlpatterns = [
    # home
    path('', views.index, name='index'),

    # login/register
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),

    # user settings/profile
    path('profile/', views.profile, name='profile'),

    # cohort stuff
    path('cohorts/', views.cohorts, name='cohorts'),
]