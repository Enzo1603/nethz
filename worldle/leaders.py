from accounts.models import CustomUser


class LeaderDatabase:
    areas_highscore = "areas_highscore"
    capitals_highscore = "capitals_highscore"
    currencies_highscore = "currencies_highscore"
    languages_highscore = "languages_highscore"


def get_leaders(highscore_db: LeaderDatabase):
    return CustomUser.objects.order_by(f"-{highscore_db}")


def get_leaders_dict(highscore_db_list: list[LeaderDatabase]):
    leaders_dict = {}
    for highscore_db in highscore_db_list:
        leaders_dict[f"{highscore_db}_leaders"] = get_leaders(highscore_db)

    return leaders_dict
