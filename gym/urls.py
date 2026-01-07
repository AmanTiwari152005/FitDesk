from django.urls import path
from .views import gym_setup_page, GymCreateAPI
from .views import CheckGymAPI,DashboardSummaryAPI
from .views import GymProfileAPI, CurrentMonthSummaryAPI


urlpatterns = [
    path('setup/', gym_setup_page),
    path('create/', GymCreateAPI.as_view()),
    path("setup/create/", GymCreateAPI.as_view()),
    path('check/', CheckGymAPI.as_view()),
    path('dashboard-data/', DashboardSummaryAPI.as_view()),
    path("profile/", GymProfileAPI.as_view()),
    path("current-month-summary/", CurrentMonthSummaryAPI.as_view()),


]
