from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from accounts.authentication import create_access_token


class ExpenseAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="owner@example.com",
            email="owner@example.com",
            password="StrongPass!2468",
        )
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {create_access_token(self.user)}"
        )

    def test_list_expenses_without_gym_returns_empty_list(self):
        response = self.client.get("/api/expenses/list/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"expenses": []})

    def test_month_detail_rejects_invalid_month(self):
        response = self.client.get("/api/expenses/month-detail/?month=bad&year=2026")

        self.assertEqual(response.status_code, 400)
