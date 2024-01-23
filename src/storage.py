from src.catching import translate_fish_name


def storage_info_message(storage_info):
    message = '*Склад*'
    empty = True
    for stored_fish in storage_info:
        stored_amount = stored_fish["stored_amount"]
        fish_name = stored_fish["fish_name"]
        if stored_amount > 0:
            empty = False
            fish_name = translate_fish_name(fish_name)
            message += f"\n- {stored_amount} {fish_name}"

    if empty:
        message = '*Склад пуст!*'

    return message


def get_player_storage(player_id, bot):
    db_connector = bot.db_connector
    storage_info = db_connector.get_player_storage(player_id)

    return storage_info_message(storage_info)
