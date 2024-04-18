from django import template
from django.templatetags.static import static

register = template.Library()


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
            "title": "Coming soon (or never)",
            "description": "nothing to be seen here",
            "button_text": "Go away",
            "image_path": static("images/informatik1_3px.jpg"),
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
