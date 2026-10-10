"""Template tags for SEO-consistent internal URLs."""

from django import template
from django.utils import translation

from lib.seo_utils import localized_path

register = template.Library()


@register.simple_tag
def localized_url(url_name, *args, **kwargs):
    """Return the canonical path for a named URL in the active language.

    Same logic as the canonical/hreflang tags in seo_meta.html, so internal
    links point at the canonical URL (e.g. German home "/" instead of the
    "/de/" alias).
    """
    return localized_path(
        url_name,
        url_args=list(args),
        url_kwargs=kwargs,
        lang_code=translation.get_language(),
    )
