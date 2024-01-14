import configparser
import random
from time import sleep

from db_requests import DBConnector

db_connector = DBConnector()


def calc_tool_catch_amount(player_id, tool):
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


def translate_fish_name(fish_name):
    match fish_name:
        case 'cod':
            fish_name = 'треска'
        case 'salmon':
            fish_name = 'лосось'
        case 'puffer':
            fish_name = 'иглобрюх'

    return fish_name


def catch_result_message(fish_caught):
    message = '**Вы поймали:**'
    for fish in fish_caught:
        caught_amount = fish["caught_amount"]
        if caught_amount > 0:
            fish_name = translate_fish_name(fish["fish_name"])
            message += f"\n- {caught_amount} {fish_name}"
    exp = calc_caught_fish_experience(fish_caught)
    message += f"\nПолучено {exp} XP"

    return message


def calc_tool_fish_caught(player_id, tool="rod"):
    fish_chances = None
    if tool == "rod":
        fish_chances = db_connector.get_player_rod_fish_catch_chances(player_id)
    elif tool == "net":
        fish_chances = db_connector.get_player_net_fish_catch_chances(player_id)

    catch_amount = calc_tool_catch_amount(player_id, tool=tool)

    fish_caught = []
    for fish_chance in fish_chances:
        fish_name = fish_chance["fish_name"]
        catch_chance = float(fish_chance["catch_chance"])
        caught_amount = int(catch_chance * catch_amount * random.uniform(0.7, 1.3))
        fish_caught.append({"fish_name": fish_name, "caught_amount": caught_amount})

    return fish_caught


def get_fish_experience(fish_name):
    fish = db_connector.get_fish(fish_name)
    experience = fish[0]["experience"]
    return experience


def get_fish_cost(fish_name):
    fish = db_connector.get_fish(fish_name)
    cost = fish[0]["cost"]
    return cost


def calc_caught_fish_experience(fish_caught):
    experience = 0
    for fish in fish_caught:
        fish_name = fish["fish_name"]
        caught_amount = fish["caught_amount"]
        fish_experience = get_fish_experience(fish_name)
        experience += caught_amount * fish_experience

    return experience


def calc_caught_fish_cost(fish_caught):
    cost = 0
    for fish in fish_caught:
        fish_name = fish["fish_name"]
        caught_amount = fish["caught_amount"]
        fish_cost = get_fish_cost(fish_name)
        cost += caught_amount * fish_cost

    return cost


def add_player_experience(player_id, amount):
    stats = db_connector.get_player_stats(player_id)
    experience = int(stats[0]["experience"] + amount)
    level = stats[0]["level"]

    exp_required = int(db_connector.get_level_exp_required(level + 1)[0]["exp_required"])
    while int(experience) >= int(exp_required):
        experience -= exp_required
        level += 1
        # сообщение о повышении уровня в диалог
        print(f"Уровень повышен до {level}!")
        exp_required = db_connector.get_level_exp_required(level + 1)[0]["exp_required"]

    db_connector.update_player_level(player_id, level)
    db_connector.update_player_experience(player_id, experience)


def update_stats(player_id, fish_caught):
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


def update_storage(player_id, fish_caught):
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


def player_catch_fish(player_id):
    fish_caught = calc_tool_fish_caught(player_id, tool="rod")
    print(catch_result_message(fish_caught))
    experience_gain = calc_caught_fish_experience(fish_caught)
    add_player_experience(player_id, experience_gain)

    update_stats(player_id, fish_caught)
    update_storage(player_id, fish_caught)


player_catch_fish(2)
