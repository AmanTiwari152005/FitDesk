from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.parsers import JSONParser
from django.core.exceptions import ValidationError
from datetime import timedelta, date

from .models import Member, MemberRenewal
from .serializers import MemberSerializer
from gym.models import Gym


# ---------------- ADD MEMBER ----------------
class AddMemberAPI(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]

    def post(self, request):
        try:
            gym = Gym.objects.get(owner=request.user)
        except Gym.DoesNotExist:
            return Response({"error": "Gym not found"}, status=400)

        serializer = MemberSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        member = serializer.save(gym=gym)

        # 💾 SAVE FIRST RENEWAL ENTRY
        fee = 0
        if member.package == "Monthly":
            fee = gym.monthly_fee
        elif member.package == "Quarterly":
            fee = gym.quarterly_fee
        elif member.package == "Yearly":
            fee = gym.yearly_fee

        MemberRenewal.objects.create(
            gym=gym,
            member=member,
            package=member.package,
            start_date=member.join_date,
            end_date=member.expiry_date,
            amount=fee
        )

        return Response({
            "success": True,
            "message": "Member added successfully",
            "gym_name": gym.gym_name,
            "member_name": member.name,
            "package": member.package,
            "join_date": member.join_date,
            "expiry_date": member.expiry_date,
        }, status=status.HTTP_201_CREATED)



# ---------------- LIST MEMBERS ----------------
class ListMembersAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        gym = Gym.objects.filter(owner=request.user).first()
        if not gym:
            return Response({"members": []})

        members = Member.objects.filter(gym=gym)
        serializer = MemberSerializer(members, many=True)
        return Response({"members": serializer.data})


# ---------------- DELETE MEMBER ----------------
class DeleteMemberAPI(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, member_id):
        try:
            gym = Gym.objects.get(owner=request.user)
            member = Member.objects.get(id=member_id, gym=gym)
        except (Gym.DoesNotExist, Member.DoesNotExist):
            return Response({"error": "Member not found"}, status=404)

        member.delete()
        return Response({"success": True})


# ---------------- RENEW MEMBER (FINAL) ----------------
class RenewMemberAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, member_id):
        gym = Gym.objects.filter(owner=request.user).first()
        if not gym:
            return Response({"error": "Gym not found"}, status=404)

        member = Member.objects.filter(id=member_id, gym=gym).first()

        if not member:
            return Response({"error": "Member not found"}, status=404)

        package = request.data.get("package")
        join_date = request.data.get("join_date")
        expiry_date = request.data.get("expiry_date")

        if not all([package, join_date, expiry_date]):
            return Response({"error": "Missing fields"}, status=400)

        valid_packages = {choice[0] for choice in Member.PACKAGE_CHOICES}
        if package not in valid_packages:
            return Response({"error": "Invalid package"}, status=400)

        member.package = package
        member.join_date = join_date
        member.expiry_date = expiry_date
        try:
            member.full_clean()
        except ValidationError as error:
            return Response({"error": error.message_dict}, status=400)
        member.save()

        # fee
        amount = 0
        if package == "Monthly":
            amount = gym.monthly_fee
        elif package == "Quarterly":
            amount = gym.quarterly_fee
        elif package == "Yearly":
            amount = gym.yearly_fee

        MemberRenewal.objects.create(
            gym=gym,
            member=member,
            package=package,
            start_date=join_date,
            end_date=expiry_date,
            amount=amount
        )

        return Response({"success": True})



# ---------------- EXPIRING SOON MEMBERS ----------------
class ExpiringSoonAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        gym = Gym.objects.filter(owner=request.user).first()
        if not gym:
            return Response({"members": []})

        today = date.today()
        upcoming = today + timedelta(days=7)

        members = Member.objects.filter(
            gym=gym,
            expiry_date__range=[today, upcoming]
        )

        data = [{
            "id": m.id,
            "name": m.name,
            "phone": m.phone,
            "expiry_date": m.expiry_date
        } for m in members]

        return Response({"members": data})
    
# ---------------- RENEWAL HISTORY ----------------
class MemberRenewalHistoryAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, member_id):
        try:
            gym = Gym.objects.get(owner=request.user)
            member = Member.objects.get(id=member_id, gym=gym)
        except (Gym.DoesNotExist, Member.DoesNotExist):
            return Response({"error": "Member not found"}, status=404)

        renewals = member.renewals.order_by("-renewed_on")

        data = []
        for r in renewals:
            data.append({
                "package": r.package,
                "start_date": r.start_date,
                "end_date": r.end_date,
                "amount": r.amount,
                "renewed_on": r.renewed_on
            })

        return Response({
            "member_name": member.name,
            "history": data
        })
