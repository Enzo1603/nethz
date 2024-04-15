from accounts.models import CustomUser


def get_leaders(highscore_type: str):
    return CustomUser.objects.order_by(f"-{highscore_type}_highscore")


def get_leaders_dict(highscore_type_list: list[str]):
    leaders_dict = {}
    for highscore_type in highscore_type_list:
        leaders_dict[f"{highscore_type}_leaders"] = get_leaders(highscore_type)

    return leaders_dict
