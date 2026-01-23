from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token

import random
from django.core.mail import send_mail
from .models import EmailOTP


# ---------------- REGISTER ----------------

class RegisterAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")

        if not all([username, email, password]):
            return Response({"success": False, "message": "All fields required"}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({"success": False, "message": "Username exists"}, status=400)

        if User.objects.filter(email=email).exists():
            return Response({"success": False, "message": "Email exists"}, status=400)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_active=False
        )

        otp = str(random.randint(100000, 999999))
        EmailOTP.objects.update_or_create(user=user, defaults={"otp": otp})

        send_mail(
            subject="Verify your FitDesk account",
            message=f"Your OTP is {otp}",
            from_email=None,
            recipient_list=[email],
            fail_silently=False
        )

        return Response({"success": True})


# ---------------- VERIFY OTP ----------------

class VerifyOTPAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")

        try:
            user = User.objects.get(email=email)
            record = EmailOTP.objects.get(user=user)
        except:
            return Response({"success": False}, status=400)

        if record.otp != otp:
            return Response({"success": False}, status=400)

        user.is_active = True
        user.save()
        record.delete()

        return Response({"success": True})


# ---------------- LOGIN (🔥 FIXED) ----------------

class LoginAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if not user:
            return Response(
                {"success": False, "message": "Invalid credentials"},
                status=401
            )

        if not user.is_active:
            return Response(
                {"success": False, "message": "Verify email first"},
                status=403
            )

        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            "success": True,
            "token": token.key   # 🔥 THIS WAS MISSING / BROKEN
        })


# ---------------- FORGOT PASSWORD ----------------

class ForgotPasswordAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        identifier = request.data.get("identifier")

        user = User.objects.filter(username=identifier).first() or \
               User.objects.filter(email=identifier).first()

        if not user:
            return Response({"success": False}, status=404)

        request.session["reset_user_id"] = user.id
        return Response({"success": True})


class ResetPasswordAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_id = request.session.get("reset_user_id")
        password = request.data.get("password")

        if not user_id or not password:
            return Response({"success": False}, status=400)

        user = User.objects.get(id=user_id)
        user.set_password(password)
        user.save()

        del request.session["reset_user_id"]
        return Response({"success": True})


# ---------------- PAGES ----------------

@ensure_csrf_cookie
def login_page(request):
    return render(request, "login.html")

def register_page(request):
    return render(request, "register.html")

def verify_otp_page(request):
    return render(request, "verify_otp.html")

def forgot_password_page(request):
    return render(request, "forgot_password.html")

def reset_password_page(request):
    return render(request, "reset_password.html")

@login_required(login_url="/api/accounts/login-page/")
def dashboard_page(request):
    return render(request, "dashboard.html")

@login_required(login_url="/api/accounts/login-page/")
def profile_page(request):
    return render(request, "profile.html")

def logout_view(request):
    logout(request)
    return redirect("/api/accounts/login-page/")
