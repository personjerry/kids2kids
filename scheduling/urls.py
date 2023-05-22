from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

app_name = 'scheduling'


urlpatterns = [
    # home
    path('', views.index, name='index'),

    path('join/<int:group_id>/', views.join_group, name='joingroup'),

    # login/register
    path('login/', LoginView.as_view(), name='login'),
    path('register/', views.register, name='register'),

    # user settings/profile
    path('profile/', views.profile, name='profile'),

    # cohort stuff
    path('cohorts/', views.cohorts, name='cohorts'),

    
]
