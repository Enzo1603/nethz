from django.db import models
from django.utils.translation import gettext_lazy as _


class ExerciseSession(models.Model):
    short_name = models.CharField(
        max_length=20,
        verbose_name=_("Short name for the exercise session"),
        help_text=_("Short name for the exercise session (e.g. TM_HS24)."),
    )

    name = models.CharField(
        max_length=100,
        verbose_name=_("Name of the exercise session"),
        help_text=_("Name of the exercise session (e.g. Engineering Mechanics HS24)."),
    )

    class Meta:
        verbose_name = _("Exercise Session")
        verbose_name_plural = _("Exercise Sessions")
        ordering = ["short_name"]

    def __str__(self):
        return f"{self.short_name} - {self.name}"


class WeekEntry(models.Model):
    NO_LINK_AVAILABLE = ""

    exercise_session = models.ForeignKey(
        ExerciseSession,
        on_delete=models.CASCADE,
        related_name="week_entries",
        verbose_name=_("Exercise Session"),
        help_text=_("The exercise session for this week entry belongs to."),
    )

    week_number = models.PositiveSmallIntegerField(
        verbose_name=_("Week Number"),
        help_text=_("The week number for this entry."),
        blank=False,
        null=False,
    )

    materials_number = models.PositiveSmallIntegerField(
        verbose_name=_("Materials Number"),
        help_text=_("The materials number for this entry."),
        blank=False,
        null=False,
    )

    exercise_materials_link = models.URLField(
        verbose_name=_("Link to the exercise materials"),
        help_text=_("Link to the exercise materials for the week."),
        blank=True,
        default=NO_LINK_AVAILABLE,
        null=False,
    )

    exercise_link = models.URLField(
        verbose_name=_("Link to the exercise"),
        help_text=_("Link to the exercise for the week."),
        blank=True,
        default=NO_LINK_AVAILABLE,
        null=False,
    )

    solutions_link = models.URLField(
        verbose_name=_("Link to the solutions"),
        help_text=_("Link to the solutions for the week."),
        blank=True,
        default=NO_LINK_AVAILABLE,
        null=False,
    )

    remarks = models.TextField(
        verbose_name=_("Remarks"),
        help_text=_("You can enter notes and remarks here. HTML is allowed."),
        blank=True,
        null=False,
        default="",
    )

    class Meta:
        verbose_name = _("Week Entry")
        verbose_name_plural = _("Week Entries")
        unique_together = ["exercise_session", "week_number"]
        ordering = ["exercise_session", "week_number"]

    def __str__(self):
        return f"{self.exercise_session.short_name} - Week {self.week_number}"

    @property
    def has_exercise_materials(self):
        return self.exercise_materials_link != self.NO_LINK_AVAILABLE

    @property
    def has_exercise(self):
        return self.exercise_link != self.NO_LINK_AVAILABLE

    @property
    def has_solutions(self):
        return self.solutions_link != self.NO_LINK_AVAILABLE
