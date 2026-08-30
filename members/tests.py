from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from accounts.authentication import create_access_token
from gym.models import Gym
from .models import Member


class MemberAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="owner@example.com",
            email="owner@example.com",
            password="StrongPass!2468",
        )
        self.gym = Gym.objects.create(
            owner=self.user,
            gym_name="FitDesk",
            address="Main Street",
            opening_time="06:00",
            closing_time="22:00",
            monthly_fee=1000,
            quarterly_fee=2500,
            yearly_fee=9000,
        )
        self.member = Member.objects.create(
            gym=self.gym,
            name="Test Member",
            phone="9999999999",
            address="Local",
            package="Monthly",
            join_date="2026-08-01",
            expiry_date="2026-09-01",
        )
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {create_access_token(self.user)}"
        )

    def test_renew_member_rejects_invalid_package(self):
        response = self.client.post(
            f"/api/members/renew/{self.member.id}/",
            {
                "package": "Lifetime",
                "join_date": "2026-09-01",
                "expiry_date": "2026-10-01",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.member.refresh_from_db()
        self.assertEqual(self.member.package, "Monthly")
