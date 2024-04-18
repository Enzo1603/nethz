from accounts.models import CustomUser


class LeaderDatabase:
    areas_highscore = "areas_highscore"
    capitals_highscore = "capitals_highscore"
    currencies_highscore = "currencies_highscore"
    languages_highscore = "languages_highscore"


def get_leaders(highscore_db: LeaderDatabase):
    return CustomUser.objects.order_by(f"-{highscore_db}")
