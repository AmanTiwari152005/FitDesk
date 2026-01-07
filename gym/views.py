from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from .models import Gym   
from django.db.models import Sum       # ✅ CORRECT
from .serializers import GymSerializer
from members.models import Member
from expenses.models import Expense
from django.utils.timezone import now
from datetime import date
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt



# ---------- PAGE VIEW ----------

def gym_setup_page(request):
    return render(request, 'gym_setup.html')


# ---------- API VIEW ----------

@method_decorator(csrf_exempt, name="dispatch")
class GymCreateAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if Gym.objects.filter(owner=request.user).exists():
            return Response({
                "success": False,
                "message": "Gym already exists"
            }, status=400)

        serializer = GymSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response({
                "success": True,
                "message": "Gym created successfully"
            })

        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=400)

    
class CheckGymAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        exists = Gym.objects.filter(owner=request.user).exists()
        return Response({
            "gym_exists": exists
        })    
    

class DashboardSummaryAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print("👤 USER:", request.user)

        gym = Gym.objects.filter(owner=request.user).first()

        if not gym:
            print("❌ NO GYM FOUND")
            return Response({
                "active_members": 0,
                "expired_members": 0,
                "total_earning": 0,
                "total_expense": 0,
                "profit": 0
            })

        print("🏋️ GYM:", gym)

        members = Member.objects.filter(gym=gym)
        print("👥 TOTAL MEMBERS:", members.count())

        today = date.today()

        active = members.filter(expiry_date__gte=today).count()
        expired = members.filter(expiry_date__lt=today).count()

        earning = 0
        for m in members:
            if m.package == "Monthly":
                earning += gym.monthly_fee
            elif m.package == "Quarterly":
                earning += gym.quarterly_fee
            elif m.package == "Yearly":
                earning += gym.yearly_fee

        expense = Expense.objects.filter(gym=gym).aggregate(
            total=Sum("amount")
        )["total"] or 0

        print("✅ ACTIVE:", active, "EXPIRED:", expired)

        return Response({
            "active_members": active,
            "expired_members": expired,
            "total_earning": earning,
            "total_expense": expense,
            "profit": earning - expense
        })   
    
class GymProfileAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        gym = Gym.objects.filter(owner=request.user).first()
        if not gym:
            return Response({"error": "Gym not found"}, status=404)

        serializer = GymSerializer(gym)
        return Response(serializer.data)

    def put(self, request):
        gym = Gym.objects.filter(owner=request.user).first()
        if not gym:
            return Response({"error": "Gym not found"}, status=404)

        serializer = GymSerializer(gym, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Gym profile updated successfully"
            })

        return Response(serializer.errors, status=400)

class CurrentMonthSummaryAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        gym = Gym.objects.filter(owner=request.user).first()
        if not gym:
            return Response({
                "earning": 0,
                "expense": 0,
                "profit": 0
            })

        today = date.today()
        month = today.month
        year = today.year

        # -------- EARNINGS --------
        members = Member.objects.filter(
            gym=gym,
            join_date__month=month,
            join_date__year=year
        )

        earning = 0
        for m in members:
            if m.package == "Monthly":
                earning += gym.monthly_fee
            elif m.package == "Quarterly":
                earning += gym.quarterly_fee
            elif m.package == "Yearly":
                earning += gym.yearly_fee

        # -------- EXPENSE --------
        expense = Expense.objects.filter(
            gym=gym,
            date__month=month,
            date__year=year
        ).aggregate(total=Sum("amount"))["total"] or 0

        return Response({
            "month": today.strftime("%B"),
            "year": year,
            "earning": earning,
            "expense": expense,
            "profit": earning - expense
        })
