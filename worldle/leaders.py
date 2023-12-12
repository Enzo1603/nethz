from accounts.models import CustomUser


def areas_leaders():
    return CustomUser.objects.order_by("-areas_highscore")
