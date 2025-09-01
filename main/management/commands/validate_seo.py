from django.core.management.base import BaseCommand
from django.test import Client
from django.urls import reverse
from django.conf import settings
import xml.etree.ElementTree as ET


class Command(BaseCommand):
    help = "Validate SEO setup including sitemap.xml and robots.txt"

    def add_arguments(self, parser):
        parser.add_argument(
            "--check-urls",
            action="store_true",
            help="Check if all sitemap URLs are accessible",
        )
        parser.add_argument(
            "--verbose",
            action="store_true",
            help="Show detailed output",
        )

    def handle(self, *args, **options):
        self.client = Client()
        self.verbose = options["verbose"]

        self.stdout.write(self.style.SUCCESS("🔍 Starting SEO validation..."))

        # Test sitemap.xml
        self.test_sitemap()

        # Test robots.txt
        self.test_robots()

        # Check individual URLs if requested
        if options["check_urls"]:
            self.check_sitemap_urls()

        self.stdout.write(self.style.SUCCESS("✅ SEO validation complete!"))

    def test_sitemap(self):
        """Test if sitemap.xml is accessible and valid"""
        self.stdout.write("\n📋 Testing sitemap.xml...")

        try:
            response = self.client.get("/sitemap.xml")

            if response.status_code == 200:
                self.stdout.write(
                    self.style.SUCCESS("  ✅ Sitemap accessible (200 OK)")
                )

                # Check if it's valid XML
                try:
                    root = ET.fromstring(response.content)
                    urls = root.findall(
                        ".//{http://www.sitemaps.org/schemas/sitemap/0.9}url"
                    )

                    self.stdout.write(
                        self.style.SUCCESS(f"  ✅ Valid XML with {len(urls)} URLs")
                    )

                    if self.verbose:
                        self.stdout.write("  📊 Sitemap breakdown:")

                        # Count URLs by type
                        static_count = 0
                        tm_count = 0
                        worldle_count = 0

                        for url in urls:
                            loc = url.find(
                                "{http://www.sitemaps.org/schemas/sitemap/0.9}loc"
                            )
                            if loc is not None:
                                url_text = loc.text
                                if (
                                    "/technische-mechanik/" in url_text
                                    and url_text.count("/") > 3
                                ):
                                    tm_count += 1
                                elif "/worldle/" in url_text and (
                                    url_text.endswith("/africa/")
                                    or url_text.endswith("/asia/")
                                    or url_text.endswith("/europe/")
                                    or url_text.endswith("/americas/")
                                    or url_text.endswith("/oceania/")
                                    or url_text.endswith("africa")
                                    or url_text.endswith("asia")
                                    or url_text.endswith("europe")
                                    or url_text.endswith("americas")
                                    or url_text.endswith("oceania")
                                ):
                                    worldle_count += 1
                                else:
                                    static_count += 1

                        self.stdout.write(f"    🏠 Static pages: {static_count}")
                        self.stdout.write(f"    📚 TM semesters: {tm_count}")
                        self.stdout.write(f"    🌍 Worldle regions: {worldle_count}")
                        self.stdout.write("")

                        for i, url in enumerate(urls[:8]):  # Show first 8 URLs
                            loc = url.find(
                                "{http://www.sitemaps.org/schemas/sitemap/0.9}loc"
                            )
                            if loc is not None:
                                self.stdout.write(f"    📍 {loc.text}")
                        if len(urls) > 8:
                            self.stdout.write(f"    ... and {len(urls) - 8} more URLs")

                except ET.ParseError as e:
                    self.stdout.write(self.style.ERROR(f"  ❌ Invalid XML: {e}"))

            else:
                self.stdout.write(
                    self.style.ERROR(
                        f"  ❌ Sitemap not accessible (Status: {response.status_code})"
                    )
                )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"  ❌ Error testing sitemap: {e}"))

    def test_robots(self):
        """Test if robots.txt is accessible and contains sitemap"""
        self.stdout.write("\n🤖 Testing robots.txt...")

        try:
            response = self.client.get("/robots.txt")

            if response.status_code == 200:
                self.stdout.write(
                    self.style.SUCCESS("  ✅ Robots.txt accessible (200 OK)")
                )

                content = response.content.decode("utf-8")

                if "Sitemap:" in content:
                    self.stdout.write(
                        self.style.SUCCESS("  ✅ Contains sitemap reference")
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING("  ⚠️  No sitemap reference found")
                    )

                if "User-agent: *" in content:
                    self.stdout.write(
                        self.style.SUCCESS("  ✅ Contains user-agent directive")
                    )

                if self.verbose:
                    self.stdout.write("\n  📄 Robots.txt content:")
                    for line in content.split("\n")[:10]:  # Show first 10 lines
                        self.stdout.write(f"    {line}")

            else:
                self.stdout.write(
                    self.style.ERROR(
                        f"  ❌ Robots.txt not accessible (Status: {response.status_code})"
                    )
                )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"  ❌ Error testing robots.txt: {e}"))

    def check_sitemap_urls(self):
        """Check if all URLs in sitemap are accessible"""
        self.stdout.write("\n🔗 Testing sitemap URLs accessibility...")

        try:
            response = self.client.get("/sitemap.xml")
            if response.status_code != 200:
                self.stdout.write(
                    self.style.ERROR("  ❌ Cannot access sitemap for URL testing")
                )
                return

            root = ET.fromstring(response.content)
            urls = root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}url")

            success_count = 0
            error_count = 0

            for url_element in urls:
                loc = url_element.find(
                    "{http://www.sitemaps.org/schemas/sitemap/0.9}loc"
                )
                if loc is not None:
                    url = loc.text
                    # Extract path from full URL
                    if url.startswith("http"):
                        from urllib.parse import urlparse

                        parsed = urlparse(url)
                        path = parsed.path
                    else:
                        path = url

                    try:
                        response = self.client.get(path)
                        if response.status_code == 200:
                            success_count += 1
                            if self.verbose:
                                self.stdout.write(self.style.SUCCESS(f"  ✅ {path}"))
                        else:
                            error_count += 1
                            self.stdout.write(
                                self.style.ERROR(
                                    f"  ❌ {path} (Status: {response.status_code})"
                                )
                            )
                    except Exception as e:
                        error_count += 1
                        self.stdout.write(self.style.ERROR(f"  ❌ {path} (Error: {e})"))

            self.stdout.write(
                f"\n📊 Results: {success_count} successful, {error_count} errors"
            )

            if error_count == 0:
                self.stdout.write(self.style.SUCCESS("  🎉 All URLs are accessible!"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"  ❌ Error checking URLs: {e}"))

    def get_site_domain(self):
        """Get the current site domain"""
        return "localhost:8000"
