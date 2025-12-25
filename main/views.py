from django.http import Http404
from django.shortcuts import render
from django.templatetags.static import static
from django.urls import reverse
from django.utils.translation import gettext as _

from .models import ExerciseSession
from django.db.models import Q
from lib.seo_utils import get_home_seo, get_technische_mechanik_seo, add_seo_to_context


def home(request):
    tm_card = {
        "title": _("Engineering Mechanics"),
        "button_text": _("To the documents"),
        "image_path": static("images/technische_mechanik_6px.webp"),
        "link": reverse("main:technische_mechanik"),
        "disable": False,
    }

    inf_card = {
        "title": _("Computer Science I 2024"),
        "button_text": _("To the documents"),
        "image_path": static("images/informatik1_3px.webp"),
        "link": "#",
        "disable": True,
    }

    worldle_card = {
        "title": "Worldle",
        "description": _("Various country quizzes"),
        "button_text": _("To the game modes"),
        "image_path": static("images/Earth_2px.webp"),
        "link": reverse("worldle:home"),
        "disable": False,
    }

    context = {
        "tm_card": tm_card,
        "inf_card": inf_card,
        "worldle_card": worldle_card,
    }

    # Add SEO data
    seo_data = get_home_seo()
    add_seo_to_context(context, seo_data, request=request, url_name="main:home")

    return render(request, "main/home.html", context)


def technische_mechanik(request, semester: str | None = None):
    # Get all available TM exercise sessions
    tm_sessions = ExerciseSession.objects.filter(
        Q(short_name__startswith="TM_")
    ).order_by("-short_name")

    if not tm_sessions.exists():
        raise Http404("No Engineering Mechanics sessions available")

    # If no semester specified, use the latest one (HS25 > HS24)
    if not semester:
        current_session = tm_sessions.first()
        current_semester = current_session.short_name.replace("TM_", "")
    else:
        template_name = f"TM_{semester}"
        current_session = tm_sessions.filter(short_name=template_name).first()
        if not current_session:
            raise Http404("Invalid semester")
        current_semester = semester

    # Get available semesters for dropdown
    available_semesters = [
        session.short_name.replace("TM_", "") for session in tm_sessions
    ]

    # Get the week entries
    week_entries = current_session.week_entries.all() if current_session else None

    context = {
        "exercise_session": current_session,
        "week_entries": week_entries,
        "current_semester": current_semester,
        "available_semesters": available_semesters,
    }

    # Add SEO data
    seo_data = get_technische_mechanik_seo(current_semester)
    if current_semester:
        add_seo_to_context(
            context, seo_data, 
            request=request, 
            url_name="main:technische_mechanik_semester",
            url_kwargs={"semester": current_semester}
        )
    else:
        add_seo_to_context(
            context, seo_data,
            request=request,
            url_name="main:technische_mechanik"
        )

    return render(request, "exercise_sessions/technische_mechanik.html", context)
