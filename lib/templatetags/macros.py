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
