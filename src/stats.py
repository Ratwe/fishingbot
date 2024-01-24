import configparser

from db_requests import DBConnector
from utils import translate_fish_name

def player_stats(player_id, bot):
    db_connector = bot.db_connector
    stats = db_connector.get_player_stats(player_id)
    level = stats[0]["level"]
    experience = stats[0]["experience"]
    next_level_experience = db_connector.get_level_exp_required(level + 1)
    balance = stats[0]["balance"]
    total_earning = stats[0]["total_earning"]
    rank = db_connector.get_player_rank(player_id)[0]["rank"]
    rod = db_connector.get_player_rod(player_id)
    cur_rod_level = rod[0]["level"]
    cur_rod_cooldown = rod[0]["cooldown"]
    config = configparser.ConfigParser()
    config.read("./settings/config.ini")
    avg_catch = int(config["Globals"]["base_catch"]) + level * float(config["Globals"]["catch_per_level"])

    message = f"*Профиль*\n" \
              f"Уровень: {level}\n" \
              f"Опыт: {experience}\n" \
              f"Опыт для следующего уровня: {next_level_experience}\n" \
              f"Баланс: {balance}\n" \
              f"Заработано всего: {total_earning}\n" \
              f"Средний улов: {avg_catch:.2f} рыб(ы)\n" \
              f"Позиция в рейтинге: {rank}\n\n"

    message += "*Ваша удочка:*\n" \
              f"Уровень: {cur_rod_level}\n" \
              f"Перезарядка: {cur_rod_cooldown:.2f} секунд(ы)\n" \
              f"Пропорция видов рыб в улове:\n"

    fish_chances = db_connector.get_player_rod_fish_catch_chances(player_id)

    for fish_chance in fish_chances:
        fish_name = fish_chance["fish_name"]
        catch_chance = float(fish_chance["catch_chance"])
        if catch_chance > 0:
            fish_name = translate_fish_name(fish_name)
            message += f"- {fish_name} {catch_chance:.2%}\n"

    message += "\nПоймано:"
    for stat in stats:
        fish_name = translate_fish_name(stat["fish_name"])
        caught_amount = stat["caught_amount"]
        if caught_amount > 0:
            message += f"\n- {caught_amount} {fish_name}"



    return message