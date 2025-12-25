from django import template
from django.templatetags.static import static
from django.utils.translation import gettext_lazy as _

register = template.Library()


class CustomMessage:
    def __init__(self, tags, message, not_dismissible=False):
        self.tags = tags
        self.message = message
        self.not_dismissible = not_dismissible

    def __str__(self):
        return self.message

    def __repr__(self):
        return self.message


@register.inclusion_tag("components/_messages.html")
def template_message(tag, message, not_dismissible=False):
    messages = [CustomMessage(tag, message, not_dismissible)]
    return {"messages": messages}


@register.inclusion_tag("macros/card.html")
def card(card_data):
    """card_data = {
    "title": "Title",
    "description": "Description",
    "button_text": "Button Text",
    "image_path": "Image/Path",
    "link": "Link",
    "disable": True/False,
    }
    """
    return card_data


@register.inclusion_tag("macros/card.html")
def coming_soon_card():
    return card(
        {
            "title": _("Coming soon (or never)"),
            "description": _("nothing to be seen here"),
            "button_text": _("Go away"),
            "image_path": static("images/informatik1_3px.webp"),
            "link": "#",
            "disable": True,
        }
    )


@register.inclusion_tag("macros/regions.html")
def region_select(region):
    return {"region": region}


@register.inclusion_tag("macros/leaderboard.html")
def leaderboard(leaderboard_config):
    return leaderboard_config


GRADIENT_PRESETS = {
    "primary": "linear-gradient(120deg, rgba(13,110,253,0.75) 0%, rgba(13,110,253,0.55) 60%)",
    "success": "linear-gradient(120deg, rgba(25,135,84,0.75) 0%, rgba(25,135,84,0.55) 60%)",
    "info": "linear-gradient(120deg, rgba(13,202,240,0.75) 0%, rgba(13,202,240,0.55) 60%)",
    "warning": "linear-gradient(120deg, rgba(255,193,7,0.8) 0%, rgba(255,193,7,0.65) 60%)",
    "danger": "linear-gradient(120deg, rgba(220,53,69,0.8) 0%, rgba(220,53,69,0.6) 60%)",
}


@register.inclusion_tag("macros/link_banner.html")
def link_banner(
    link,
    title,
    icon,
    gradient="primary",
    subtitle="",
    icon_color="",
    target="_blank",
):
    """
    Usage:
        {% link_banner link="https://example.com" title="Title" icon="bi-icon" gradient="primary" %}

    Gradient presets: primary, success, info, warning, danger
    Or use a custom gradient string.

    If icon_color is not specified, it defaults to the gradient preset name.
    """
    # Resolve gradient preset or use as-is
    resolved_gradient = GRADIENT_PRESETS.get(gradient, gradient)

    # Default icon_color to gradient name if it's a preset
    if not icon_color:
        icon_color = gradient if gradient in GRADIENT_PRESETS else "primary"

    return {
        "link": link,
        "title": title,
        "subtitle": subtitle,
        "icon": icon,
        "icon_color": icon_color,
        "gradient": resolved_gradient,
        "target": target,
    }
