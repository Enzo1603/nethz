from django.http import JsonResponse
from django.test import TestCase
from django.urls import reverse

from worldle.views import DEFAULT_REGION


# Create your tests here.
class WorldleViewsTest(TestCase):
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

    def test_areas_view(self):
        response = self.client.get(reverse("worldle:areas"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "worldle/areas.html")

        # Add more assertions for the content of the response, if needed

    def test_get_country_view(self):
        response = self.client.get(reverse("worldle:get_country"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)

        # Add more assertions for the content of the response, if needed
        json_data = response.json()
        self.assertIn("country", json_data)
        country = json_data["country"]
        self.assertIsInstance(country, dict)

        # Ensure that the country has the expected fields
        expected_fields = {
            "name.common",
            "cca3",
            "area",
        }
        self.assertTrue(expected_fields.issubset(country.keys()))

    # Add more test cases as needed
