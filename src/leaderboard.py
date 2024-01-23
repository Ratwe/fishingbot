def leaderboard_message(player_id, leaderboard, db_connector):
    message = "*Таблица лидеров*\n" \
              "Ранг. Имя (уровень): Всего заработано\n"
    count = 0
    for record in leaderboard and count < 20:
        cur_player_id = record["player_id"]
        player_name = db_connector.get_player_name(cur_player_id)[0]["name"]
        rank = record["rank"]
        stats = db_connector.get_player_stats(cur_player_id)
        level = stats[0]["level"]
        total_earning = stats[0]["total_earning"]

        message += f"{rank}. @{player_name} ({level}): {total_earning}$\n"
        count += 1

    stats = db_connector.get_player_stats(player_id)
    player_name = db_connector.get_player_name(player_id)[0]["name"]
    rank = db_connector.get_player_rank(player_id)[0]["rank"]
    level = stats[0]["level"]
    total_earning = stats[0]["total_earning"]

    message += "\nВаша позиция:\n" \
               f"{rank}. @{player_name} ({level}): {total_earning}$\n"

    return message


def get_leaderboard(player_id, bot):
    db_connector = bot.db_connector

    leaderboard = db_connector.get_leaderboard()

    return leaderboard_message(player_id, leaderboard, db_connector)
