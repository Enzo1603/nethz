from django.core.management.base import BaseCommand
from django.test import Client


class Command(BaseCommand):
    help = "Validate basic SEO setup (sitemap and robots.txt)"

    def handle(self, *args, **options):
        self.client = Client()

        self.stdout.write("🔍 Checking SEO setup...\n")

        # Test sitemap.xml
        self.test_sitemap()

        # Test robots.txt
        self.test_robots()

        self.stdout.write(self.style.SUCCESS("✅ SEO check complete!"))

    def test_sitemap(self):
        """Test if sitemap.xml works"""
        try:
            response = self.client.get("/sitemap.xml")

            if response.status_code == 200:
                # Count URLs in sitemap
                content = response.content.decode()
                url_count = content.count("<url>")

                self.stdout.write(
                    self.style.SUCCESS(f"✅ Sitemap works ({url_count} URLs)")
                )
            else:
                self.stdout.write(
                    self.style.ERROR(
                        f"❌ Sitemap failed (Status: {response.status_code})"
                    )
                )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Sitemap error: {e}"))

    def test_robots(self):
        """Test if robots.txt works"""
        try:
            response = self.client.get("/robots.txt")

            if response.status_code == 200:
                content = response.content.decode()
                has_sitemap = "Sitemap:" in content

                if has_sitemap:
                    self.stdout.write(
                        self.style.SUCCESS("✅ Robots.txt works (includes sitemap)")
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING("⚠️  Robots.txt works (no sitemap reference)")
                    )
            else:
                self.stdout.write(
                    self.style.ERROR(
                        f"❌ Robots.txt failed (Status: {response.status_code})"
                    )
                )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Robots.txt error: {e}"))
