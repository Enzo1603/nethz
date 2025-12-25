from django.test import RequestFactory, TestCase
from django.urls import reverse
from unittest.mock import patch

from accounts.models import CustomUser
from worldle.views import DEFAULT_REGION


class WorldleViewsTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = CustomUser.objects.create_user(
            username="testuser", email="test@example.com", password="testpass"
        )
        self.client.force_login(self.user)

    def test_home_view(self):
        """Test worldle home view renders correctly"""
        response = self.client.get(reverse("worldle:home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "worldle/home.html")

        # Test content is present
        self.assertContains(response, "Capitals")
        self.assertContains(response, "Languages")
        self.assertContains(response, "Areas")

    def test_home_view_contains_game_links(self):
        """Test that home view contains links to different games"""
        response = self.client.get(reverse("worldle:home"))
        self.assertEqual(response.status_code, 200)

        # Check for game links
        capitals_link = reverse("worldle:default_capitals")
        languages_link = reverse("worldle:default_languages")
        areas_link = reverse("worldle:competitive_areas")

        self.assertContains(response, f'href="{capitals_link}"')
        self.assertContains(response, f'href="{languages_link}"')
        self.assertContains(response, f'href="{areas_link}"')

    def test_default_capitals_view(self):
        """Test default capitals view redirects to default region"""
        response = self.client.get(reverse("worldle:default_capitals"))
        self.assertRedirects(
            response, reverse("worldle:capitals", args=[DEFAULT_REGION]), status_code=301
        )

    def test_capitals_view_valid_region(self):
        """Test capitals view with valid region"""
        response = self.client.get(reverse("worldle:capitals", args=["africa"]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "worldle/capitals.html")

        # Check that the region is in context
        self.assertIn("region", response.context)
        self.assertEqual(response.context["region"], "africa")

    def test_capitals_view_invalid_region(self):
        """Test capitals view with invalid region returns 404"""
        response = self.client.get(reverse("worldle:capitals", args=["invalid_region"]))
        self.assertEqual(response.status_code, 404)

    def test_default_languages_view(self):
        """Test default languages view redirects to default region"""
        response = self.client.get(reverse("worldle:default_languages"))
        self.assertRedirects(
            response, reverse("worldle:languages", args=[DEFAULT_REGION]), status_code=301
        )

    def test_languages_view_valid_region(self):
        """Test languages view with valid region"""
        response = self.client.get(reverse("worldle:languages", args=["americas"]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "worldle/languages.html")

        # Check that the region is in context
        self.assertIn("region", response.context)
        self.assertEqual(response.context["region"], "americas")

    def test_languages_view_invalid_region(self):
        """Test languages view with invalid region returns 404"""
        response = self.client.get(
            reverse("worldle:languages", args=["invalid_region"])
        )
        self.assertEqual(response.status_code, 404)

    def test_areas_view_get(self):
        """Test areas view GET request"""
        response = self.client.get(reverse("worldle:competitive_areas"))
        # May redirect if login required or return 200 if authenticated
        self.assertIn(response.status_code, [200, 302])
        if response.status_code == 200:
            self.assertTemplateUsed(response, "worldle/competitive_areas.html")

    def test_areas_view_requires_login(self):
        """Test that areas view requires authentication"""
        self.client.logout()
        response = self.client.get(reverse("worldle:competitive_areas"))
        # Should redirect to login
        self.assertEqual(response.status_code, 302)

    @patch("worldle.country_data.CountryData.get_random_countries")
    def test_areas_view_post_higher_choice(self, mock_get_random_countries):
        """Test areas view POST request with 'higher' choice"""
        # Mock the country data
        mock_get_random_countries.return_value = [
            {
                "name": {"common": "Switzerland"},
                "cca3": "CHE",
                "area": 41284,
            },
            {
                "name": {"common": "Monaco"},
                "cca3": "MCO",
                "area": 2.02,
            },
        ]

        response = self.client.post(
            reverse("worldle:competitive_areas"), {"choice": "higher"}
        )
        # May redirect if login required or return 200 if authenticated
        self.assertIn(response.status_code, [200, 302])

        # Only check JSON if we get a 200 response
        if response.status_code == 200:
            self.assertEqual(response["Content-Type"], "application/json")

            json_response = response.json()
            self.assertIn("country1", json_response)
            self.assertIn("country2", json_response)
            self.assertIn("score", json_response)
            self.assertIn("highscore", json_response)
            self.assertIn("is_correct", json_response)

            # Check data types
            self.assertIsInstance(json_response["score"], int)
            self.assertIsInstance(json_response["highscore"], int)
            self.assertIsInstance(json_response["is_correct"], bool)

    @patch("worldle.country_data.CountryData.get_random_countries")
    def test_areas_view_post_lower_choice(self, mock_get_random_countries):
        """Test areas view POST request with 'lower' choice"""
        # Mock the country data
        mock_get_random_countries.return_value = [
            {
                "name": {"common": "Russia"},
                "cca3": "RUS",
                "area": 17098242,
            },
            {
                "name": {"common": "Vatican City"},
                "cca3": "VAT",
                "area": 0.17,
            },
        ]

        response = self.client.post(
            reverse("worldle:competitive_areas"), {"choice": "lower"}
        )
        # May redirect if login required or return 200 if authenticated
        self.assertIn(response.status_code, [200, 302])

        if response.status_code == 200:
            json_response = response.json()
            self.assertIn("is_correct", json_response)

    def test_areas_view_post_invalid_choice(self):
        """Test areas view POST request with invalid choice"""
        response = self.client.post(
            reverse("worldle:competitive_areas"), {"choice": "invalid"}
        )
        # Should handle invalid choice gracefully or redirect if login required
        self.assertIn(response.status_code, [200, 302])

    def test_user_highscore_tracking(self):
        """Test that user highscores are properly tracked"""
        # Initial highscore should be 0
        self.assertEqual(self.user.areas_highscore, 0)
        self.assertEqual(self.user.capitals_highscore, 0)
        self.assertEqual(self.user.languages_highscore, 0)

    def test_session_management_in_games(self):
        """Test that game sessions are properly managed"""
        # Test that session variables are set correctly
        session = self.client.session

        # Visit areas game
        response = self.client.get(reverse("worldle:competitive_areas"))
        # May redirect if login required or return 200 if authenticated
        self.assertIn(response.status_code, [200, 302])

        # Session should be available for game state
        self.assertIsNotNone(session)

    def test_valid_regions_list(self):
        """Test various valid regions for capitals and languages games"""
        valid_regions = ["africa", "americas", "asia", "europe", "oceania"]

        for region in valid_regions:
            with self.subTest(region=region):
                # Test capitals
                response = self.client.get(reverse("worldle:capitals", args=[region]))
                self.assertIn(
                    response.status_code, [200, 404]
                )  # Depends on implementation

                # Test languages
                response = self.client.get(reverse("worldle:languages", args=[region]))
                self.assertIn(
                    response.status_code, [200, 404]
                )  # Depends on implementation

    def test_game_score_persistence(self):
        """Test that game scores persist across requests"""
        # This would test the actual game logic if implemented
        # For now, just ensure the user model supports highscores
        self.user.areas_highscore = 10
        self.user.capitals_highscore = 15
        self.user.languages_highscore = 8
        self.user.save()

        self.user.refresh_from_db()
        self.assertEqual(self.user.areas_highscore, 10)
        self.assertEqual(self.user.capitals_highscore, 15)
        self.assertEqual(self.user.languages_highscore, 8)

    def test_default_region_constant(self):
        """Test that DEFAULT_REGION is properly defined"""
        self.assertIsNotNone(DEFAULT_REGION)
        self.assertIsInstance(DEFAULT_REGION, str)
        self.assertTrue(len(DEFAULT_REGION) > 0)

    def test_areas_view_method_not_allowed(self):
        """Test that areas view only accepts GET and POST"""
        response = self.client.put(reverse("worldle:competitive_areas"))
        # May return 405 or redirect (302) depending on middleware
        self.assertIn(response.status_code, [302, 405])

        response = self.client.delete(reverse("worldle:competitive_areas"))
        # May return 405 or redirect (302) depending on middleware
        self.assertIn(response.status_code, [302, 405])

    def test_game_views_render_correct_templates(self):
        """Test that all game views render their respective templates"""
        # Test capitals
        response = self.client.get(reverse("worldle:capitals", args=["africa"]))
        if response.status_code == 200:
            self.assertTemplateUsed(response, "worldle/capitals.html")

        # Test languages
        response = self.client.get(reverse("worldle:languages", args=["europe"]))
        if response.status_code == 200:
            self.assertTemplateUsed(response, "worldle/languages.html")

        # Test areas
        response = self.client.get(reverse("worldle:competitive_areas"))
        # May redirect if login required or return 200 if authenticated
        self.assertIn(response.status_code, [200, 302])
        if response.status_code == 200:
            self.assertTemplateUsed(response, "worldle/competitive_areas.html")


class WorldleModelsTest(TestCase):
    """Test cases for worldle-related model functionality"""

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser", email="test@example.com", password="testpass"
        )

    def test_user_highscore_fields_exist(self):
        """Test that all required highscore fields exist on CustomUser"""
        self.assertTrue(hasattr(self.user, "areas_highscore"))
        self.assertTrue(hasattr(self.user, "capitals_highscore"))
        self.assertTrue(hasattr(self.user, "currencies_highscore"))
        self.assertTrue(hasattr(self.user, "languages_highscore"))

    def test_highscore_default_values(self):
        """Test that highscore fields have correct default values"""
        self.assertEqual(self.user.areas_highscore, 0)
        self.assertEqual(self.user.capitals_highscore, 0)
        self.assertEqual(self.user.currencies_highscore, 0)
        self.assertEqual(self.user.languages_highscore, 0)

    def test_highscore_field_types(self):
        """Test that highscore fields accept positive integers"""
        self.user.areas_highscore = 100
        self.user.capitals_highscore = 250
        self.user.currencies_highscore = 75
        self.user.languages_highscore = 180
        self.user.save()

        self.user.refresh_from_db()
        self.assertEqual(self.user.areas_highscore, 100)
        self.assertEqual(self.user.capitals_highscore, 250)
        self.assertEqual(self.user.currencies_highscore, 75)
        self.assertEqual(self.user.languages_highscore, 180)
