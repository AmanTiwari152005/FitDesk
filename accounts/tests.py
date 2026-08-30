from django.contrib.auth.models import User
from django.test import override_settings
from rest_framework.test import APITestCase

from .authentication import create_access_token


class RegistrationTests(APITestCase):
    register_url = "/api/accounts/register/"
    login_url = "/api/accounts/login/"
    reset_password_url = "/api/accounts/reset-password/"

    def test_registers_active_user_with_email_and_hashed_password(self):
        response = self.client.post(
            self.register_url,
            {"email": "Owner@Example.com", "password": "StrongPass!2468"},
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        user = User.objects.get(email="owner@example.com")
        self.assertEqual(user.username, "owner@example.com")
        self.assertTrue(user.is_active)
        self.assertTrue(user.check_password("StrongPass!2468"))

    def test_registration_rejects_duplicate_email_ignoring_case(self):
        User.objects.create_user(
            username="owner@example.com",
            email="owner@example.com",
            password="StrongPass!2468",
        )

        response = self.client.post(
            self.register_url,
            {"email": "OWNER@example.com", "password": "AnotherPass!2468"},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(User.objects.count(), 1)

    def test_login_accepts_email_and_returns_token(self):
        User.objects.create_user(
            username="owner@example.com",
            email="owner@example.com",
            password="StrongPass!2468",
        )

        response = self.client.post(
            self.login_url,
            {"email": "OWNER@example.com", "password": "StrongPass!2468"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["token"])
        self.assertEqual(response.data["token_type"], "Bearer")
        self.assertEqual(len(response.data["token"].split(".")), 3)

    def test_password_reset_requires_identifier_for_logged_out_user(self):
        user = User.objects.create_user(
            username="owner@example.com",
            email="owner@example.com",
            password="StrongPass!2468",
        )

        response = self.client.post(
            self.reset_password_url,
            {
                "password": "NewStrongPass!2468",
            },
            format="json",
        )

        user.refresh_from_db()
        self.assertEqual(response.status_code, 400)
        self.assertTrue(user.check_password("StrongPass!2468"))

    @override_settings(DEBUG=True)
    def test_logged_out_user_can_reset_with_identifier_in_learning_mode(self):
        user = User.objects.create_user(
            username="owner@example.com",
            email="owner@example.com",
            password="StrongPass!2468",
        )

        response = self.client.post(
            self.reset_password_url,
            {
                "identifier": "OWNER@example.com",
                "password": "NewStrongPass!2468",
            },
            format="json",
        )

        user.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(user.check_password("NewStrongPass!2468"))

    @override_settings(DEBUG=False, SECRET_KEY="test-secret-key")
    def test_logged_out_password_reset_is_disabled_outside_learning_mode(self):
        user = User.objects.create_user(
            username="owner@example.com",
            email="owner@example.com",
            password="StrongPass!2468",
        )

        response = self.client.post(
            self.reset_password_url,
            {
                "identifier": "owner@example.com",
                "password": "NewStrongPass!2468",
            },
            format="json",
        )

        user.refresh_from_db()
        self.assertEqual(response.status_code, 400)
        self.assertTrue(user.check_password("StrongPass!2468"))

    def test_authenticated_password_change_requires_current_password(self):
        user = User.objects.create_user(
            username="owner@example.com",
            email="owner@example.com",
            password="StrongPass!2468",
        )
        login_response = self.client.post(
            self.login_url,
            {"email": "owner@example.com", "password": "StrongPass!2468"},
            format="json",
        )
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {login_response.data['token']}"
        )

        response = self.client.post(
            self.reset_password_url,
            {
                "current_password": "WrongPass!2468",
                "password": "NewStrongPass!2468",
            },
            format="json",
        )

        user.refresh_from_db()
        self.assertEqual(response.status_code, 400)
        self.assertTrue(user.check_password("StrongPass!2468"))

    def test_authenticated_user_can_change_password(self):
        user = User.objects.create_user(
            username="owner@example.com",
            email="owner@example.com",
            password="StrongPass!2468",
        )
        login_response = self.client.post(
            self.login_url,
            {"email": "owner@example.com", "password": "StrongPass!2468"},
            format="json",
        )
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {login_response.data['token']}"
        )

        response = self.client.post(
            self.reset_password_url,
            {
                "current_password": "StrongPass!2468",
                "password": "NewStrongPass!2468",
            },
            format="json",
        )

        user.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(user.check_password("NewStrongPass!2468"))

    def test_password_change_invalidates_existing_jwt(self):
        user = User.objects.create_user(
            username="owner@example.com",
            email="owner@example.com",
            password="StrongPass!2468",
        )
        token = create_access_token(user)
        user.set_password("NewStrongPass!2468")
        user.save(update_fields=["password"])

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.post(
            self.reset_password_url,
            {
                "current_password": "NewStrongPass!2468",
                "password": "AnotherStrongPass!2468",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 403)
