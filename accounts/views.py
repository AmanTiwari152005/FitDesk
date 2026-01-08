

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework import status
import random
from django.core.mail import send_mail
from .models import EmailOTP
from django.views.decorators.csrf import ensure_csrf_cookie



# -------------------------------------------------
# ---------------- API VIEWS ----------------------
# -------------------------------------------------

class VerifyOTPAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")

        try:
            user = User.objects.get(email=email)
            record = EmailOTP.objects.get(user=user)
        except:
            return Response({"message": "Invalid request"}, status=400)

        if record.otp != otp:
            return Response({"message": "Invalid OTP"}, status=400)

        user.is_active = True
        user.save()
        record.delete()

        return Response({
            "success": True,
            "message": "Account verified successfully"
        })


class RegisterAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")

        if not all([username, email, password]):
            return Response({"message": "All fields required"}, status=400)

        if User.objects.filter(email=email).exists():
            return Response({"message": "Email already exists"}, status=400)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_active=False   # 🔥 IMPORTANT
        )

        otp = str(random.randint(100000, 999999))

        EmailOTP.objects.update_or_create(
            user=user,
            defaults={"otp": otp}
        )

        send_mail(
            subject="Verify your account",
            message=f"Your verification code is {otp}",
            from_email=None,
            recipient_list=[email],
        )

        return Response({
            "success": True,
            "message": "OTP sent to email"
        })



# class LoginAPI(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         username = request.data.get("username")
#         password = request.data.get("password")

#         if not username or not password:
#             return Response({
#                 "success": False,
#                 "message": "Username and password required"
#             }, status=400)

#         user = authenticate(username=username, password=password)

#         if user is None:
#             return Response({
#                 "success": False,
#                 "message": "Invalid credentials"
#             }, status=401)

#         token, _ = Token.objects.get_or_create(user=user)

#         return Response({
#             "success": True,
#             "token": token.key
#         })
class LoginAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        print("🔥 LOGIN API HIT")
        print("📦 DATA:", request.data)

        try:
            username = request.data.get("username")
            password = request.data.get("password")

            print("👤 USERNAME:", username)

            user = authenticate(username=username, password=password)
            print("✅ AUTH RESULT:", user)

            if user is None:
                return Response(
                    {"success": False, "message": "Invalid credentials"},
                    status=401
                )

            token, _ = Token.objects.get_or_create(user=user)

            return Response({
                "success": True,
                "token": token.key
            })

        except Exception as e:
            print("❌ LOGIN CRASH:", str(e))
            raise


from django.contrib.auth.models import User

class ForgotPasswordAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        identifier = request.data.get("identifier")

        if not identifier:
            return Response({"success": False, "message": "Required"}, status=400)

        user = User.objects.filter(username=identifier).first() \
            or User.objects.filter(email=identifier).first()

        if not user:
            return Response({"success": False, "message": "User not found"}, status=404)

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






# -------------------------------------------------
# ---------------- PAGE VIEWS ---------------------
# -------------------------------------------------
@ensure_csrf_cookie
def login_page(request):
    print("LOGIN PAGE HIT:", request.method, request.path)
    return render(request, "login.html")


def register_page(request):
    print("REGISTER PAGE HIT:", request.method, request.path)
    return render(request, "register.html")



def profile_page(request):
    return render(request, "profile.html")


def add_expense_page(request):
    return render(request, "add_expense.html")

def verify_otp_page(request):
    return render(request, "verify_otp.html")

def forgot_password_page(request):
    return render(request, "forgot_password.html")

def reset_password_page(request):
    return render(request, "reset_password.html")
