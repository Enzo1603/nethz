from django.test import TestCase
from django.urls import reverse
from django.templatetags.static import static


# Create your tests here.
class MainViewsTest(TestCase):
    def test_home_view(self):
        response = self.client.get(reverse("main:home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/home.html")

        # Add more assertions for the content of the response, if needed
        self.assertContains(response, "Engineering Mechanics 2024")
        self.assertContains(response, "Computer Science I 2024")
        self.assertContains(response, "Worldle")

    def test_technische_mechanik_view(self):
        response_valid = self.client.get(
            reverse("main:technische_mechanik", args=["HS24"])
        )
        self.assertEqual(response_valid.status_code, 200)
        self.assertTemplateUsed(response_valid, "technische_mechanik/TM_HS24.html")

        response_invalid = self.client.get(
            reverse("main:technische_mechanik", args=["InvalidSemester"])
        )
        self.assertEqual(response_invalid.status_code, 404)

    def test_home_view_card_links(self):
        response = self.client.get(reverse("main:home"))
        self.assertEqual(response.status_code, 200)

        # Test that the links in the cards are correct
        self.assertContains(
            response,
            'href="' + reverse("main:technische_mechanik", args=["HS24"]) + '"',
        )
        self.assertContains(
            response,
            'href="#"',  # You may want to update this once you have a valid link for ph_card and inf_card
        )
        self.assertContains(response, 'href="' + reverse("worldle:home") + '"')

    def test_home_view_card_images(self):
        response = self.client.get(reverse("main:home"))
        self.assertEqual(response.status_code, 200)

        # Test that the image paths in the cards are correct
        self.assertContains(
            response,
            'src="' + static("images/technische_mechanik_6px.jpg") + '"',
        )
        self.assertContains(
            response,
            'src="' + static("images/informatik1_3px.jpg") + '"',
        )
        self.assertContains(
            response,
            'src="' + static("images/Earth_2px.jpg") + '"',
        )
