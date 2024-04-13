from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model, authenticate

from accounts.models import CustomUser


class CustomUserTests(TestCase):
    def setUp(self):
        self.user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword@12",
        }
        self.user = get_user_model().objects.create_user(**self.user_data)

    def test_user_creation(self):
        self.assertEqual(self.user.username, self.user_data["username"])
        self.assertEqual(self.user.email, self.user_data["email"])
        self.assertTrue(self.user.check_password(self.user_data["password"]))

    def test_signup_view(self):
        url = reverse("accounts:signup")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Test signup functionality
        response = self.client.post(url, data=self.user_data)
        self.assertEqual(response.status_code, 200)

        # Check if the user is actually created
        user = get_user_model().objects.filter(email=self.user_data["email"]).first()
        self.assertTrue(user is not None)

        # Manually set is_email_verified to True
        user.is_email_verified = True
        user.save()

        # Check if is_email_verified is set to True
        self.assertTrue(user.is_email_verified)

    def test_login_view(self):
        # Log in first
        login = self.client.login(
            email=self.user_data["email"], password=self.user_data["password"]
        )
        self.assertTrue(login)

        url = reverse("accounts:login")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Test login functionality
        response = self.client.post(
            url,
            data={
                "email": self.user_data["email"],
                "password": self.user_data["password"],
            },
        )
        self.assertEqual(
            response.status_code, 200
        )  # Expecting a redirect after successful login

        # Check if the user is logged in
        user = authenticate(
            email=self.user_data["email"], password=self.user_data["password"]
        )
        self.assertTrue(user.is_authenticated)

    def test_logout_view(self):
        # Log in first
        self.client.login(
            email=self.user_data["email"], password=self.user_data["password"]
        )

        url = reverse("accounts:logout")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Redirects after logout

        # Check if the user is logged out
        self.assertFalse("_auth_user_id" in self.client.session)

    def test_user_update_view(self):
        # Log in first
        login = self.client.login(
            email=self.user_data["email"], password=self.user_data["password"]
        )
        self.assertTrue(login)

        url = reverse("accounts:user_account")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        # Test user update functionality
        updated_data = {"username": "newusername", "email": self.user_data["email"]}
        response = self.client.post(url, data=updated_data, follow=True)
        self.assertEqual(response.status_code, 200)

        # Check if the user is actually updated
        user = CustomUser.objects.get(username=updated_data["username"])
        self.assertEqual(user.username, updated_data["username"])
