from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include
from django.shortcuts import redirect


urlpatterns = [
    path("", lambda request: redirect("/api/accounts/login-page/")),
    # ---------------- ADMIN ----------------
    path("admin/", admin.site.urls),

    # ---------------- FRONTEND PAGES ----------------
    path("dashboard/", lambda r: render(r, "dashboard.html")),
    path("add-member/", lambda r: render(r, "add_member.html")),
    path("members/", lambda r: render(r, "members.html")),
    path("add-expense/", lambda r: render(r, "add_expense.html")),
    path("renewal-history/", lambda r: render(r, "renewal_history.html")),
    path("api/gym/setup/", lambda r: render(r, "gym_setup.html")),


    # Allauth removed: accounts/ route no longer provided by django-allauth

    # ---------------- API ROUTES ----------------
    path("api/accounts/", include("accounts.urls")),          # your custom login/register pages
    #path("api/accounts/", include("dj_rest_auth.urls")),      # token login/logout
    

    path("api/gym/", include("gym.urls")),
    path("api/members/", include("members.urls")),
    path("api/expenses/", include("expenses.urls")),
]
