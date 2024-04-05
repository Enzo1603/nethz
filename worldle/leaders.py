from accounts.models import CustomUser


def areas_leaders():
    return CustomUser.objects.order_by("-areas_highscore")


def capitals_leaders():
    return CustomUser.objects.order_by("-capitals_highscore")


def languages_leaders():
    return CustomUser.objects.order_by("-languages_highscore")
