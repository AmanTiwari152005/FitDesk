from django.conf import settings
from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .authentication import create_access_token
from .serializers import RegisterSerializer


# ---------------- REGISTER ----------------

class RegisterAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            message = next(iter(serializer.errors.values()))[0]
            return Response({"success": False, "message": str(message)}, status=400)

        serializer.save()
        return Response(
            {"success": True, "message": "Account created successfully."},
            status=201,
        )


# ---------------- LOGIN ----------------

class LoginAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = str(request.data.get("email", "")).strip().lower()
        password = request.data.get("password")

        account = User.objects.filter(email__iexact=email).first()
        username = account.username if account else email
        user = authenticate(username=username, password=password)

        if not user:
            return Response(
                {"success": False, "message": "Invalid credentials"},
                status=401
            )

        token = create_access_token(user)

        return Response({
            "success": True,
            "token": token,
            "access": token,
            "token_type": "Bearer",
        })


# ---------------- FORGOT PASSWORD ----------------

class ForgotPasswordAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        return Response({
            "success": True,
            "message": "Continue to reset password.",
        })


class ResetPasswordAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        identifier = str(request.data.get("identifier", "")).strip().lower()
        current_password = request.data.get("current_password")
        new_password = request.data.get("password")

        user = request.user if request.user.is_authenticated else None

        if user and current_password:
            if not new_password:
                return Response({
                    "success": False,
                    "message": "New password is required."
                }, status=400)

            if not user.check_password(current_password):
                return Response({
                    "success": False,
                    "message": "Current password is incorrect."
                }, status=400)
        else:
            if not settings.DEBUG:
                return Response({
                    "success": False,
                    "message": "Password reset without verification is available only in local learning mode."
                }, status=400)

            if not identifier or not new_password:
                return Response({
                    "success": False,
                    "message": "Email or username and new password are required."
                }, status=400)

            user = User.objects.filter(email__iexact=identifier).first() or \
                   User.objects.filter(username__iexact=identifier).first()

            if not user:
                return Response({
                    "success": False,
                    "message": "Account not found."
                }, status=400)

        if not new_password:
            return Response({
                "success": False,
                "message": "New password is required."
            }, status=400)

        try:
            validate_password(new_password, user)
        except ValidationError as error:
            return Response({
                "success": False,
                "message": error.messages[0] if error.messages else "Invalid password."
            }, status=400)

        user.set_password(new_password)
        user.save(update_fields=["password"])
        return Response({"success": True})


# ---------------- PAGES ----------------

@ensure_csrf_cookie
def login_page(request):
    return render(request, "login.html")

def register_page(request):
    return render(request, "register.html")

def forgot_password_page(request):
    return render(request, "forgot_password.html")

def reset_password_page(request):
    return render(request, "reset_password.html")

def dashboard_page(request):
    return render(request, "dashboard.html")

def profile_page(request):
    return render(request, "profile.html")

def logout_view(request):
    logout(request)
    return redirect("/api/accounts/login-page/")
