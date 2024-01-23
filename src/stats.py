from db_requests import DBConnector
from src.utils import translate_fish_name

db_connector = DBConnector()


def player_stats(player_id):
    stats = db_connector.get_player_stats(player_id)
    level = stats[0]["level"]
    experience = stats[0]["experience"]
    balance = stats[0]["balance"]
    total_earning = stats[0]["total_earning"]
    rank = db_connector.get_player_rank(player_id)[0]["rank"]

    message = f"*Профиль*\n" \
              f"Уровень: {level}\n" \
              f"Опыт: {experience}\n" \
              f"Баланс: {balance}\n" \
              f"Заработано всего: {total_earning}\n" \
              f"Позиция в рейтинге: {rank}\n\n"

    message += "Поймано:"
    for stat in stats:
        fish_name = translate_fish_name(stat["fish_name"])
        caught_amount = stat["caught_amount"]
        if caught_amount > 0:
            message += f"\n- {caught_amount} {fish_name}"

    return message