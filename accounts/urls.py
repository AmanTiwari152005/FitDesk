from django.urls import path
from .views import ForgotPasswordAPI, RegisterAPI, LoginAPI, ResetPasswordAPI, forgot_password_page, login_page, register_page, VerifyOTPAPI, reset_password_page
#from .views import GoogleLoginAPI

from . import views

urlpatterns = [
    # API endpoints
    path('register/', RegisterAPI.as_view()),
    path('login/', LoginAPI.as_view()),
    path("verify-otp/", VerifyOTPAPI.as_view()),
    path("forgot-password/", ForgotPasswordAPI.as_view()),
    path("reset-password/", ResetPasswordAPI.as_view()),
   # path("google-login/", GoogleLoginAPI.as_view()),
   


    # Frontend pages
    path('login-page/', login_page,name='login'),
    path('register-page/', register_page,name='register'),
    path("profile/", views.profile_page, name="profile"),
    path("add-expense/", views.add_expense_page),
    path("verify-otp-page/", views.verify_otp_page),
    path("forgot-password-page/", forgot_password_page),
    path("reset-password-page/", reset_password_page),

]
