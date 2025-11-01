from django.conf import settings
from django.http import HttpResponse


def robots_txt(request):
    """
    Generiert robots.txt dynamisch mit korrekter Domain.
    """
    # Bestimme die korrekte Domain
    scheme = "https" if request.is_secure() else "http"
    domain = request.get_host()
    sitemap_url = f"{scheme}://{domain}/sitemap.xml"

    lines = [
        "User-agent: *",
        "Allow: /",
        "",
        "# Sitemap location",
        f"Sitemap: {sitemap_url}",
        "",
        "# Disallow admin and private areas",
        "Disallow: /admin/",
        "Disallow: /de/accounts/",
        "Disallow: /en/accounts/",
        "",
        "# Allow important pages",
        "Allow: /de/",
        "Allow: /en/",
        "Allow: /de/worldle/",
        "Allow: /en/worldle/",
        "Allow: /de/technische-mechanik/",
        "Allow: /en/technische-mechanik/",
    ]

    return HttpResponse("\n".join(lines), content_type="text/plain")
