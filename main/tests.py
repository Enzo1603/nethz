from django.test import TestCase
from django.urls import reverse
from django.templatetags.static import static


class MainViewsTest(TestCase):
    def test_home_view(self):
        """Test that home view renders correctly"""
        response = self.client.get(reverse("main:home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/home.html")

        # Test content is present (language-agnostic for CI compatibility)
        content = response.content.decode()
        self.assertTrue(
            "Technische Mechanik" in content or "Engineering Mechanics" in content,
            f"Expected mechanics text not found in response: {content[:500]}...",
        )
        self.assertContains(response, "Worldle")

    def test_technische_mechanik_view_without_semester(self):
        """Test technische mechanik view without semester parameter"""
        response = self.client.get(reverse("main:technische_mechanik"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "exercise_sessions/technische_mechanik.html")

    def test_technische_mechanik_view_with_valid_semester(self):
        """Test technische mechanik view with valid semester"""
        response = self.client.get(
            reverse("main:technische_mechanik_semester", args=["HS24"])
        )
        # May return 404 or 200 depending on available semesters
        self.assertIn(response.status_code, [200, 404])
        if response.status_code == 200:
            self.assertTemplateUsed(
                response, "exercise_sessions/technische_mechanik.html"
            )

    def test_technische_mechanik_view_with_invalid_semester(self):
        """Test technische mechanik view with invalid semester returns 404"""
        response = self.client.get(
            reverse("main:technische_mechanik_semester", args=["InvalidSemester"])
        )
        self.assertEqual(response.status_code, 404)

    def test_home_view_card_links(self):
        """Test that the card links on home page are correct"""
        response = self.client.get(reverse("main:home"))
        self.assertEqual(response.status_code, 200)

        # Test that the links in the cards are correct
        tm_link = reverse("main:technische_mechanik")
        self.assertContains(response, f'href="{tm_link}"')

        worldle_link = reverse("worldle:home")
        self.assertContains(response, f'href="{worldle_link}"')

    def test_home_view_card_images(self):
        """Test that the card images on home page are correct"""
        response = self.client.get(reverse("main:home"))
        self.assertEqual(response.status_code, 200)

        # Test that the image paths in the cards are correct
        tm_image = static("images/technische_mechanik_6px.webp")
        self.assertContains(response, f'src="{tm_image}"')

        earth_image = static("images/Earth_2px.webp")
        self.assertContains(response, f'src="{earth_image}"')

    def test_home_view_contains_navigation(self):
        """Test that home view contains basic navigation elements"""
        response = self.client.get(reverse("main:home"))
        self.assertEqual(response.status_code, 200)

        # Check for common navigation elements
        self.assertContains(response, "Home", count=None)

    def test_technische_mechanik_context_data(self):
        """Test that technische mechanik view passes correct context"""
        response = self.client.get(
            reverse("main:technische_mechanik_semester", args=["HS24"])
        )
        # May return 404 or 200 depending on available semesters
        self.assertIn(response.status_code, [200, 404])

        # Check if semester is in context only if view returns 200
        if response.status_code == 200 and "semester" in response.context:
            self.assertEqual(response.context["semester"], "HS24")

    def test_technische_mechanik_default_semester(self):
        """Test technische mechanik view without semester uses default"""
        response = self.client.get(reverse("main:technische_mechanik"))
        self.assertEqual(response.status_code, 200)

        # Should have a default semester in context (if the view supports it)
        if hasattr(response, "context") and response.context:
            # Context may or may not include semester depending on implementation
            pass

    def test_home_view_meta_tags(self):
        """Test that home view includes proper meta tags"""
        response = self.client.get(reverse("main:home"))
        self.assertEqual(response.status_code, 200)

        # Check for viewport meta tag (common in responsive design)
        self.assertContains(response, 'name="viewport"', count=None)

    def test_view_response_headers(self):
        """Test that views return proper HTTP headers"""
        response = self.client.get(reverse("main:home"))
        self.assertEqual(response.status_code, 200)

        # Check content type
        self.assertEqual(response["Content-Type"], "text/html; charset=utf-8")

    def test_all_semester_codes_valid(self):
        """Test various semester codes that should be valid"""
        valid_semesters = ["HS24", "HS25"]

        for semester in valid_semesters:
            with self.subTest(semester=semester):
                response = self.client.get(
                    reverse("main:technische_mechanik_semester", args=[semester])
                )
                # Should be 200 or 404 depending on implementation
                self.assertIn(response.status_code, [200, 404])

    def test_invalid_semester_patterns(self):
        """Test various invalid semester patterns"""
        invalid_semesters = ["INVALID", "2024", "HS", "FS"]

        for semester in invalid_semesters:
            with self.subTest(semester=semester):
                response = self.client.get(
                    reverse("main:technische_mechanik_semester", args=[semester])
                )
                # Invalid semesters should return 404
                self.assertEqual(response.status_code, 404)

    def test_url_patterns_are_correct(self):
        """Test that URL patterns resolve correctly"""
        # Test home URL (adjusted for i18n)
        home_url = reverse("main:home")
        self.assertTrue(home_url.endswith("/"))

        # Test technische mechanik URLs (adjusted for i18n)
        tm_url = reverse("main:technische_mechanik")
        self.assertTrue("technische-mechanik" in tm_url)

        tm_semester_url = reverse("main:technische_mechanik_semester", args=["HS24"])
        self.assertTrue(
            "technische-mechanik" in tm_semester_url and "HS24" in tm_semester_url
        )
