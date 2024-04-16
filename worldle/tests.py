# from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory, TestCase
from django.urls import reverse

# from unittest.mock import patch

from accounts.models import CustomUser
from worldle.views import DEFAULT_REGION  # , areas


# Create your tests here.
class WorldleViewsTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = CustomUser.objects.create_user(
            username="testuser", password="testpass"
        )
        self.client.force_login(self.user)

    def test_home_view(self):
        response = self.client.get(reverse("worldle:home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "worldle/home.html")

        # Add more assertions for the content of the response, if needed
        self.assertContains(response, "Capitals")
        self.assertContains(response, "Languages")
        self.assertContains(response, "Areas")

    def test_default_capitals_view(self):
        response = self.client.get(reverse("worldle:default_capitals"))
        self.assertRedirects(
            response, reverse("worldle:capitals", args=[DEFAULT_REGION])
        )

    def test_capitals_view(self):
        # Test with a valid region
        response = self.client.get(reverse("worldle:capitals", args=["africa"]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "worldle/capitals.html")

        # Test with an invalid region
        response_invalid = self.client.get(
            reverse(
                "main:technische_mechanik",
                args=["invalid_region"],
            ),
        )
        self.assertEqual(response_invalid.status_code, 404)

        # Add more test cases as needed

    def test_default_languages_view(self):
        response = self.client.get(reverse("worldle:default_languages"))
        self.assertRedirects(
            response, reverse("worldle:languages", args=[DEFAULT_REGION])
        )

    def test_languages_view(self):
        # Test with a valid region
        response = self.client.get(reverse("worldle:languages", args=["americas"]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "worldle/languages.html")

        # Test with an invalid region
        response_invalid = self.client.get("worldle:languages", args=["invalid_region"])
        self.assertEqual(response_invalid.status_code, 404)

        # Add more test cases as needed

    # @patch("worldle.country_data.CountryData.get_random_countries")
    # def test_areas_view(self, mock_get_random_countries):
    #     # Mocking get_random_countries to return fixed countries for testing
    #     mock_get_random_countries.return_value = [
    #         {
    #             "name.common": "Switzerland",
    #             "cca3": "CHE",
    #             "area": "41284",
    #         },
    #         {
    #             "name.common": "United States Minor Outlying Islands",
    #             "cca3": "UMI",
    #             "area": "34.2",
    #         },
    #     ]

    #     response = self.client.get(reverse("worldle:areas"))
    #     # self.assertTemplateUsed(response, "worldle/areas.html")

    #     request = self.factory.get(reverse("worldle:areas"))
    #     middleware = SessionMiddleware(lambda x: None)
    #     middleware.process_request(request)
    #     request.user = self.user

    #     response = areas(request)

    #     self.assertEqual(response.status_code, 200)

    #     # Add more assertions for the content of the response, if needed

    #     # Example assertions for the JSON response in a POST request
    #     response_post = self.client.post(reverse("worldle:areas"), {"choice": "higher"})
    #     json_response = response_post.json()

    #     self.assertIn("country1", json_response)
    #     self.assertIn("country2", json_response)
    #     self.assertIn("score", json_response)
    #     self.assertIn("highscore", json_response)
    #     self.assertIn("is_correct", json_response)
    #     self.assertTrue(isinstance(json_response["score"], int))
    #     self.assertTrue(isinstance(json_response["highscore"], int))
    #     self.assertTrue(isinstance(json_response["is_correct"], bool))
