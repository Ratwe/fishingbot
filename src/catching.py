import configparser
import random

from datetime import datetime

from utils import translate_fish_name


def calc_tool_catch_amount(player_id, db_connector, tool="rod"):
    player_stats = db_connector.get_player_stats(player_id)
    player_level = int(player_stats[0]["level"])
    config = configparser.ConfigParser()
    config.read("./settings/config.ini")
    catch_amount = int(config["Globals"]["base_catch"]) + player_level * float(config["Globals"]["catch_per_level"])

    if tool == "net":
        net = db_connector.get_player_net(player_id)
        catch_coef = net[0]["catch_coef"]
        catch_amount *= catch_coef

    return catch_amount

def catch_result_message(fish_caught, db_connector):
    message = '*Вы поймали:*'
    for fish in fish_caught:
        caught_amount = fish["caught_amount"]
        if caught_amount > 0:
            fish_name = translate_fish_name(fish["fish_name"])
            message += f"\n- {caught_amount} {fish_name}"
    exp = calc_caught_fish_experience(fish_caught, db_connector)
    message += f"\nПолучено {exp} XP"

    return message


async def can_player_fish(player_id, msg_time, bot, tool="rod"):
    db_connector = bot.db_connector
    last_usages = db_connector.get_player_last_usages(player_id)
    last_usage: datetime = None
    cooldown: int = None
    if tool == "rod":
        rod = db_connector.get_player_rod(player_id)
        cooldown = rod[0]["cooldown"]
        last_usage = last_usages[0]["rod_last_use"]
    elif tool == "net":
        net = db_connector.get_player_net(player_id)
        cooldown = net[0]["cooldown"]
        last_usage = last_usages[0]["net_last_use"]

    if last_usage is not None:
        msg_time_str = msg_time.strftime('%Y-%m-%d %H:%M:%S')
        last_usage_str = last_usage.strftime('%Y-%m-%d %H:%M:%S')
        msg_time = datetime.strptime(msg_time_str, "%Y-%m-%d %H:%M:%S")
        last_usage = datetime.strptime(last_usage_str, "%Y-%m-%d %H:%M:%S")

        diff = (msg_time - last_usage).total_seconds()

        if diff < cooldown:
            await bot.send_cooldown_message(player_id, cooldown - diff, tool)
            return False

    return True


def calc_tool_fish_caught(player_id, db_connector, tool="rod"):
    fish_chances = None
    if tool == "rod":
        fish_chances = db_connector.get_player_rod_fish_catch_chances(player_id)
    elif tool == "net":
        fish_chances = db_connector.get_player_net_fish_catch_chances(player_id)

    catch_amount = calc_tool_catch_amount(player_id, db_connector, tool=tool)

    fish_caught = []
    for fish_chance in fish_chances:
        fish_name = fish_chance["fish_name"]
        catch_chance = float(fish_chance["catch_chance"])
        caught_amount = int(catch_chance * catch_amount * random.uniform(0.7, 1.3))
        fish_caught.append({"fish_name": fish_name, "caught_amount": caught_amount})

    if tool == "net":
        print("net fish_caught:", fish_caught)

    return fish_caught


def get_fish_experience(fish_name, db_connector):
    fish = db_connector.get_fish(fish_name)
    experience = fish[0]["experience"]
    return experience


def get_fish_cost(fish_name, db_connector):
    fish = db_connector.get_fish(fish_name)
    cost = fish[0]["cost"]
    return cost


def calc_caught_fish_experience(fish_caught, db_connector):
    experience = 0
    for fish in fish_caught:
        fish_name = fish["fish_name"]
        caught_amount = fish["caught_amount"]
        fish_experience = get_fish_experience(fish_name, db_connector)
        experience += caught_amount * fish_experience

    return experience


def calc_caught_fish_cost(fish_caught, db_connector):
    cost = 0
    for fish in fish_caught:
        fish_name = fish["fish_name"]
        caught_amount = fish["caught_amount"]
        fish_cost = get_fish_cost(fish_name, db_connector)
        cost += caught_amount * fish_cost

    return cost


async def add_player_experience(player_id, amount, bot):
    db_connector = bot.db_connector
    stats = db_connector.get_player_stats(player_id)
    experience = int(stats[0]["experience"] + amount)
    level = stats[0]["level"]

    exp_required = int(db_connector.get_level_exp_required(level + 1)[0]["exp_required"])
    while int(experience) >= int(exp_required):
        experience -= exp_required
        level += 1
        db_connector.update_player_level(player_id, level)
        db_connector.update_player_experience(player_id, experience)
        # сообщение о повышении уровня в диалог
        print(f"Уровень игрока {player_id} повышен до {level}!")
        exp_required = db_connector.get_level_exp_required(level + 1)[0]["exp_required"]
        await bot.send_message(player_id, f"Уровень повышен до {level}!")

    db_connector.update_player_experience(player_id, experience)


def update_stats(player_id, fish_caught, db_connector):
    for fish in fish_caught:
        fish_name = fish["fish_name"]
        fish_caught_gain = fish["caught_amount"]

        fish_caught_id = db_connector.get_fish_caught_id(player_id, fish_name)[0]["id"]
        fish_caught = db_connector.get_player_fish_caught(player_id)
        cur_fish_caught_amount = None
        for cur_fish_caught in fish_caught:
            if cur_fish_caught["fish_name"] == fish_name:
                cur_fish_caught_amount = cur_fish_caught["caught_amount"]
        db_connector.update_fish_caught(fish_caught_id, cur_fish_caught_amount + fish_caught_gain)


def update_storage(player_id, fish_caught, db_connector):
    for fish in fish_caught:
        fish_name = fish["fish_name"]
        fish_stored_gain = fish["caught_amount"]

        fish_stored_id = db_connector.get_fish_stored_id(player_id, fish_name)[0]["id"]
        fish_stored = db_connector.get_player_fish_stored(player_id)
        cur_fish_stored_amount = None
        for cur_fish_stored in fish_stored:
            if cur_fish_stored["fish_name"] == fish_name:
                cur_fish_stored_amount = cur_fish_stored["stored_amount"]
        db_connector.update_fish_stored(fish_stored_id, cur_fish_stored_amount + fish_stored_gain)


async def get_player_catch_fish(player_id, msg_date: datetime, bot, tool="rod"):
    if await can_player_fish(player_id, msg_date, bot, tool=tool):
        fish_caught = calc_tool_fish_caught(player_id, bot.db_connector, tool=tool)
        experience_gain = calc_caught_fish_experience(fish_caught, bot.db_connector)

        update_stats(player_id, fish_caught, bot.db_connector)
        update_storage(player_id, fish_caught, bot.db_connector)
        bot.db_connector.update_tool_last_use(player_id, msg_date, tool=tool)

        await add_player_experience(player_id, experience_gain, bot)
    else:
        return None

    return catch_result_message(fish_caught, bot.db_connector)
