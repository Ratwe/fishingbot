from utils import translate_fish_name


def calc_fish_profit(fish_name, amount, db_connector):
    fish_cost = db_connector.get_fish(fish_name)[0]["cost"]
    return amount * fish_cost


def get_profit_message(storage_info, db_connector, total_profit):
    if total_profit == 0:
        return "Нечего продавать!\nНачать рыбачить - /fish"

    message = "*Продано:*\n"

    for stored_fish in storage_info:
        stored_amount = stored_fish["stored_amount"]
        fish_name = stored_fish["fish_name"]

        if stored_amount > 0:
            profit = calc_fish_profit(fish_name, stored_amount, db_connector)
            fish_name = translate_fish_name(fish_name)
            message += f"- {stored_amount} {fish_name} за *{profit}*$\n"

    message += f"\nВсего получено *{total_profit}$*"
    return message


def calc_storage_profit(storage_info, db_connector):
    total_profit = 0

    for stored_fish in storage_info:
        stored_amount = stored_fish["stored_amount"]
        fish_name = stored_fish["fish_name"]

        if stored_amount > 0:
            profit = calc_fish_profit(fish_name, stored_amount, db_connector)
            total_profit += profit

    return total_profit


def sell_storage(player_id, storage_info, db_connector):
    profit = calc_storage_profit(storage_info, db_connector)

    db_connector.sell_storage(player_id, profit)

    return get_profit_message(storage_info, db_connector, profit)


def sell_all(player_id, bot):
    db_connector = bot.db_connector
    storage_info = db_connector.get_player_storage(player_id)

    return sell_storage(player_id, storage_info, db_connector)
