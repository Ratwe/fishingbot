from utils import translate_fish_name


def up_rod(player_id, bot):
    db_connector = bot.db_connector
    rod = db_connector.get_player_rod(player_id)
    cur_rod_level = rod[0]["level"]
    cur_rod_cooldown = rod[0]["cooldown"]
    next_level_rod = db_connector.get_rod_by_level(cur_rod_level + 1)
    next_level_rod_cooldown = next_level_rod[0]["cooldown"]
    rod_price = next_level_rod[0]["price"]

    message = "*Ваша удочка:*\n" \
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

    message += "\n*Улучшение удочки:*\n" \
               f"Уровень: {cur_rod_level + 1}\n" \
               f"Перезарядка: {next_level_rod_cooldown:.2f} секунд(ы)\n" \
               f"Пропорция видов рыб в улове:\n"

    fish_chances = db_connector.get_rod_fish_catch_chances(cur_rod_level + 1)

    for fish_chance in fish_chances:
        fish_name = fish_chance["fish_name"]
        catch_chance = float(fish_chance["catch_chance"])
        if catch_chance > 0:
            fish_name = translate_fish_name(fish_name)
            message += f"- {fish_name} {catch_chance:.2%}\n"

    message += f"\nЦена: *{rod_price}$*"

    return message


def up_rod_approve(player_id, bot):
    db_connector = bot.db_connector
    rod = db_connector.get_player_rod(player_id)
    balance = db_connector.get_player_balance(player_id)[0]["balance"]
    cur_rod_level = rod[0]["level"]
    next_level_rod = db_connector.get_rod_by_level(cur_rod_level + 1)
    rod_price = next_level_rod[0]["price"]
    player_level = db_connector.get_player_level(player_id)[0]["level"]

    if player_level >= cur_rod_level + 1:
        if balance >= rod_price:
            db_connector.up_player_rod(player_id, cur_rod_level + 1, delta=-rod_price)
            return f"Удочка улучшена до *{cur_rod_level + 1} уровня* за *{rod_price}$*!"
        else:
            return f"Недостаточно средств! На счету всего {balance}, а нужно {rod_price}!"
    else:
        return f"Необходим {cur_rod_level + 1} уровень!"


def up_net(player_id, bot):
    db_connector = bot.db_connector
    net = db_connector.get_player_net(player_id)
    cur_net_level = net[0]["level"]
    cur_net_cooldown = net[0]["cooldown"]
    cur_net_catch_coef = net[0]["catch_coef"]
    next_level_net = db_connector.get_net_by_level(cur_net_level + 1)
    next_level_net_cooldown = next_level_net[0]["cooldown"]
    next_level_net_catch_coef = next_level_net[0]["catch_coef"]
    net_price = next_level_net[0]["price"]

    message = "*Ваша сеть:*\n" \
              f"Уровень: {cur_net_level}\n" \
              f"Перезарядка: {cur_net_cooldown:.2f} секунд(ы)\n" \
              f"Коэффициент улова: x{cur_net_catch_coef}\n" \
              f"Пропорция видов рыб в улове:\n"

    fish_chances = db_connector.get_player_net_fish_catch_chances(player_id)

    for fish_chance in fish_chances:
        fish_name = fish_chance["fish_name"]
        catch_chance = float(fish_chance["catch_chance"])
        if catch_chance > 0:
            fish_name = translate_fish_name(fish_name)
            message += f"- {fish_name} {catch_chance:.2%}\n"

    message += "\n*Улучшение сети:*\n" \
               f"Уровень: {cur_net_level + 1}\n" \
               f"Перезарядка: {next_level_net_cooldown:.2f} секунд(ы)\n" \
               f"Коэффициент улова: x{next_level_net_catch_coef}\n" \
               f"Пропорция видов рыб в улове:\n"

    fish_chances = db_connector.get_net_fish_catch_chances(cur_net_level + 1)

    for fish_chance in fish_chances:
        fish_name = fish_chance["fish_name"]
        catch_chance = float(fish_chance["catch_chance"])
        if catch_chance > 0:
            fish_name = translate_fish_name(fish_name)
            message += f"- {fish_name} {catch_chance:.2%}\n"

    message += f"\nЦена: *{net_price}$*"

    return message


def up_net_approve(player_id, bot):
    db_connector = bot.db_connector
    net = db_connector.get_player_net(player_id)
    balance = db_connector.get_player_balance(player_id)[0]["balance"]
    cur_net_level = net[0]["level"]
    next_level_net = db_connector.get_net_by_level(cur_net_level + 1)
    net_price = next_level_net[0]["price"]
    player_level = db_connector.get_player_level(player_id)[0]["level"]

    if player_level >= cur_net_level + 1:
        if balance >= net_price:
            db_connector.up_player_net(player_id, cur_net_level + 1, delta=-net_price)
            return f"Сеть улучшена до *{cur_net_level + 1} уровня* за *{net_price}$*!"
        else:
            return f"Недостаточно средств! На счету всего {balance}, а нужно {net_price}!"
    else:
        return f"Необходим {cur_net_level + 1} уровень!"
