from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models.functions import TruncMonth
from django.db.models.functions import ExtractMonth, ExtractYear
from .models import Expense
from members.models import Member
from django.db.models import Sum
from .serializers import ExpenseSerializer
from gym.models import Gym


class AddExpenseAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            gym = Gym.objects.get(owner=request.user)
        except Gym.DoesNotExist:
            return Response(
                {"error": "Gym not found"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(gym=gym)
            return Response(
                {"message": "Expense added successfully"},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListExpenseAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        gym = Gym.objects.get(owner=request.user)
        expenses = Expense.objects.filter(gym=gym)
        serializer = ExpenseSerializer(expenses, many=True)

        return Response({"expenses": serializer.data})
    
class MonthlyExpenseSummaryAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        gym = Gym.objects.filter(owner=request.user).first()
        if not gym:
            return Response([])

        expenses = (
            Expense.objects.filter(gym=gym)
            .annotate(month=ExtractMonth("date"), year=ExtractYear("date"))
            .values("month", "year")
            .annotate(total_expense=Sum("amount"))
            .order_by("-year", "-month")
        )

        month_names = [
            "", "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]

        result = []

        for e in expenses:
            month = e["month"]
            year = e["year"]

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

            result.append({
                "month": month_names[month],
                "year": year,
                "earning": earning,
                "expense": e["total_expense"],
                "profit": earning - e["total_expense"]
            })

        return Response(result) 

class MonthDetailAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        month = int(request.GET.get("month"))
        year = int(request.GET.get("year"))

        gym = Gym.objects.get(owner=request.user)

        expenses = Expense.objects.filter(
            gym=gym,
            date__month=month,
            date__year=year
        )

        expense_total = expenses.aggregate(
            total=Sum("amount")
        )["total"] or 0

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

        return Response({
            "month": month,
            "year": year,
            "earning": earning,
            "expense": expense_total,
            "profit": earning - expense_total,
            "expenses": [
                {
                    "title": e.title,
                    "amount": e.amount,
                    "date": e.date
                } for e in expenses
            ]
        })
