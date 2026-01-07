from django.urls import path
from .views import AddExpenseAPI, ListExpenseAPI,MonthlyExpenseSummaryAPI,MonthDetailAPI

urlpatterns = [
    path('add/', AddExpenseAPI.as_view()),
    path('list/', ListExpenseAPI.as_view()),
    path("monthly-summary/", MonthlyExpenseSummaryAPI.as_view()),
    path("month-detail/", MonthDetailAPI.as_view()),
]
