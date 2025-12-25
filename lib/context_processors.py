import tomllib
from datetime import datetime, timezone
from pathlib import Path
from functools import lru_cache

from django.conf import settings
from django.urls import reverse


@lru_cache(maxsize=1)
def get_version():
    """Get version from pyproject.toml, cached for performance."""
    try:
        pyproject_path = Path(__file__).resolve().parent.parent / "pyproject.toml"
        with open(pyproject_path, "rb") as f:
            data = tomllib.load(f)
        return data.get("project", {}).get("version", "unknown")
    except Exception:
        return "unknown"


def get_absolute_url(request, url_name, *args, **kwargs):
    """Generate absolute URL for a given URL name."""
    scheme = "https" if request.is_secure() else "http"
    host = request.get_host()
    # Get the current language from the request path
    path = reverse(url_name, args=args, kwargs=kwargs)
    return f"{scheme}://{host}{path}"


def get_hreflang_urls(request, url_name, *args, **kwargs):
    """Generate hreflang URLs for all languages."""
    scheme = "https" if request.is_secure() else "http"
    host = request.get_host()
    hreflang_urls = {}
    
    from django.utils import translation
    
    # Save current language
    current_lang = translation.get_language()
    
    try:
        for lang_code, _lang_name in getattr(settings, "LANGUAGES", ()):
            with translation.override(lang_code):
                path = reverse(url_name, args=args, kwargs=kwargs)
                hreflang_urls[lang_code] = f"{scheme}://{host}{path}"
    finally:
        # Restore original language
        translation.activate(current_lang)
    
    return hreflang_urls


def inject_global_context(request):
    return {
        "utcnow": datetime.now(timezone.utc),
        "version": get_version(),
        "request": request,  # Make request available in templates for URL generation
    }
