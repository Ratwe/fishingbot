import configparser

import psycopg2


def execute_query(query):
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result


def fetch_as_dicts(query):
    cursor = conn.cursor()
    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    result = [dict(zip(columns, row)) for row in cursor.fetchall()]
    cursor.close()
    return result


def get_player_rod_fish_catch_chances(player_id):
    query = '''
    SELECT fish_name, catch_chance
    FROM fish_chances
    WHERE rod_level = (SELECT player.rod_level FROM player WHERE player_id = {player_id});
    '''.format(player_id=player_id)
    return fetch_as_dicts(query)


def get_player_net_fish_catch_chances(player_id):
    query = '''
    SELECT fish_name, catch_chance
    FROM fish_chances
    WHERE rod_level = (SELECT player.net_level FROM player WHERE player_id = {player_id});
    '''.format(player_id=player_id)
    return fetch_as_dicts(query)


def get_leaderboard():
    query = '''
    SELECT * FROM leaderboard
    '''
    return fetch_as_dicts(query)


def get_player_rank(player_id):
    query = '''
    SELECT id, rank FROM leaderboard WHERE player_id = {player_id}
    '''.format(player_id=player_id)
    return fetch_as_dicts(query)


def get_player_fish_stored(player_id):
    query = '''
    SELECT fish_name, stored_amount
    FROM player
    JOIN storage ON player.player_id = storage.player_id
    JOIN fish_stored ON storage.id = fish_stored.storage_id
    WHERE player.player_id = {player_id};
    '''.format(player_id=player_id)
    return fetch_as_dicts(query)


def get_player_storage(player_id):
    query = '''
    SELECT storage_id, fish_name, stored_amount
    FROM player
    JOIN storage ON player.player_id = storage.player_id
    JOIN fish_stored ON storage.id = fish_stored.storage_id
    WHERE player.player_id = {player_id}
    '''.format(player_id=player_id)
    return fetch_as_dicts(query)


def get_player_fish_caught(player_id):
    query = '''
    SELECT fish_name, caught_amount
    FROM player
    JOIN stats ON player.player_id = stats.player_id
    JOIN fish_caught ON stats.id = fish_caught.stats_id
    WHERE player.player_id = {player_id};
    '''.format(player_id=player_id)
    return fetch_as_dicts(query)


def get_player_stats(player_id):
    query = '''
    SELECT level, experience, stats.id as stats_id, total_earning, balance, fish_name, caught_amount
    FROM player
    JOIN stats ON player.player_id = stats.player_id
    JOIN fish_caught ON stats.id = fish_caught.stats_id
    WHERE player.player_id = {player_id};
    '''.format(player_id=player_id)
    return fetch_as_dicts(query)


def get_promoted_channels():
    query = '''
    SELECT * FROM promoted_channels
    '''
    return fetch_as_dicts(query)


conn = None
try:
    config = configparser.ConfigParser()
    config.read("settings/config.ini")
    conn = psycopg2.connect(dbname=config["Database"]["dbname"], user=config["Database"]["user"],
                            password=config["Database"]["pass"], host=config["Database"]["hostname"],
                            port=config["Database"]["port"])
except Exception as e:
    print(f'Error: {e}')

if conn:
    print("Player Rod Fish Catch Chances:", get_player_rod_fish_catch_chances(2))
    print("Player Net Fish Catch Chances:", get_player_net_fish_catch_chances(2))
    print("Leaderboard:", get_leaderboard())
    print("Player Rank:", get_player_rank(2))
    print("Player Fish Stored:", get_player_fish_stored(2))
    print("Player Storage:", get_player_storage(2))
    print("Player Fish Caught:", get_player_fish_caught(2))
    print("Player Stats:", get_player_stats(2))
    print("Promoted Channels:", get_promoted_channels())
    conn.close()
