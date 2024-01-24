import configparser

import psycopg2


class DBConnector:

    def __init__(self):
        self.config = self.read_config()
        self.conn = psycopg2.connect(
            dbname=self.config["Database"]["dbname"],
            user=self.config["Database"]["user"],
            password=self.config["Database"]["pass"],
            host=self.config["Database"]["hostname"],
            port=self.config["Database"]["port"]
        )

    def __del__(self):
        if self.conn is not None:
            self.conn.close()
            print("DB connection closed")

    def read_config(self):
        config = configparser.ConfigParser()
        config.read("./settings/config.ini")
        return config

    def execute_query(self, query, commit=True):
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            # Получение результатов запроса
            cursor.close()
            if commit:
                self.conn.commit()
        except Exception as e:
            print(f"Error executing query: {str(e)}")
            self.conn.rollback()

    def fetch_as_dicts(self, query):
        cursor = self.conn.cursor()
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]
        cursor.close()
        return result

    def get_rod_fish_catch_chances(self, level):
        query = f'''
        SELECT fish_name, catch_chance
        FROM fish_chances
        WHERE rod_level = {level};
        '''
        return self.fetch_as_dicts(query)

    def get_net_fish_catch_chances(self, level):
        query = f'''
        SELECT fish_name, catch_chance
        FROM fish_chances
        WHERE net_level = {level};
        '''
        return self.fetch_as_dicts(query)

    def get_player_rod_fish_catch_chances(self, player_id):
        query = f'''
        SELECT fish_name, catch_chance
        FROM fish_chances
        WHERE rod_level = (SELECT player.rod_level FROM player WHERE player_id = {player_id});
        '''
        return self.fetch_as_dicts(query)

    def get_player_net_fish_catch_chances(self, player_id):
        query = f'''
        SELECT fish_name, catch_chance
        FROM fish_chances
        WHERE net_level = (SELECT player.net_level FROM player WHERE player_id = {player_id});
        '''
        return self.fetch_as_dicts(query)

    def get_player_last_usages(self, player_id):
        query = f'''
        SELECT *
        FROM last_usages
        WHERE player_id = {player_id};
        '''
        return self.fetch_as_dicts(query)

    def update_tool_last_use(self, player_id, time, tool):
        query = f'''
        UPDATE last_usages
        SET {tool}_last_use = '{time}'
        WHERE player_id = {player_id}
        '''
        self.execute_query(query)

    def get_leaderboard(self):
        query = '''
        SELECT * FROM leaderboard
        '''
        return self.fetch_as_dicts(query)

    def get_player_rank(self, player_id):
        query = f'''
        SELECT id, rank FROM leaderboard WHERE player_id = {player_id}'''
        return self.fetch_as_dicts(query)

    def get_player_fish_stored(self, player_id):
        query = f'''
        SELECT fish_name, stored_amount
        FROM player
        JOIN storage ON player.player_id = storage.player_id
        JOIN fish_stored ON storage.id = fish_stored.storage_id
        WHERE player.player_id = {player_id};
        '''
        return self.fetch_as_dicts(query)

    def get_player_storage(self, player_id):
        query = f'''
        SELECT storage_id, fish_name, stored_amount
        FROM player
        JOIN storage ON player.player_id = storage.player_id
        JOIN fish_stored ON storage.id = fish_stored.storage_id
        WHERE player.player_id = {player_id}
        '''
        return self.fetch_as_dicts(query)

    def get_player_fish_caught(self, player_id):
        query = f'''
        SELECT fish_name, caught_amount
        FROM player
        JOIN stats ON player.player_id = stats.player_id
        JOIN fish_caught ON stats.id = fish_caught.stats_id
        WHERE player.player_id = {player_id};
        '''
        return self.fetch_as_dicts(query)

    def get_player_stats(self, player_id):
        query = f'''
        SELECT level, experience, stats.id as stats_id, total_earning, balance, fish_name, caught_amount
        FROM player
        JOIN stats ON player.player_id = stats.player_id
        JOIN fish_caught ON stats.id = fish_caught.stats_id
        WHERE player.player_id = {player_id};
        '''
        return self.fetch_as_dicts(query)

    def get_player_balance(self, player_id):
        query = f'''
        SELECT balance
        FROM player
        JOIN stats ON player.player_id = stats.player_id
        WHERE player.player_id = {player_id};
        '''
        return self.fetch_as_dicts(query)

    def get_promoted_channels(self):
        query = '''
        SELECT * FROM promoted_channels
        '''
        return self.fetch_as_dicts(query)

    def get_fish(self, fish_name):
        query = f'''
        SELECT * FROM fish WHERE fish_name = '{fish_name}'
        '''
        return self.fetch_as_dicts(query)

    def get_player_name(self, player_id):
        query = f'''
        SELECT name FROM player
        WHERE player_id = {player_id};
        '''
        return self.fetch_as_dicts(query)

    def get_player_net(self, player_id):
        query = f'''
        SELECT * FROM net
        WHERE level = (SELECT player.net_level FROM player WHERE player_id = {player_id});
        '''
        return self.fetch_as_dicts(query)

    def get_player_rod(self, player_id):
        query = f'''
        SELECT * FROM rod
        WHERE level = (SELECT player.rod_level FROM player WHERE player_id = {player_id});
        '''
        return self.fetch_as_dicts(query)

    def get_player_level(self, player_id):
        query = f'''
           SELECT level FROM player
           WHERE player_id = {player_id};
           '''
        return self.fetch_as_dicts(query)

    def get_rod_by_level(self, level):
        query = f'''
        SELECT * FROM rod
        WHERE level = {level};
        '''
        return self.fetch_as_dicts(query)

    def get_net_by_level(self, level):
        query = f'''
        SELECT * FROM net
        WHERE level = {level};
        '''
        return self.fetch_as_dicts(query)

    def get_levels(self):
        query = '''SELECT * FROM levels'''
        return self.fetch_as_dicts(query)

    def get_level_exp_required(self, level):
        query = f'''SELECT exp_required FROM levels WHERE level = {level}'''
        return self.fetch_as_dicts(query)

    def update_player_level(self, player_id, level):
        query = f'''UPDATE player
                SET level = {level}
                WHERE player_id = {player_id}
                '''
        self.execute_query(query)

    def update_player_experience(self, player_id, experience):
        query = f'''UPDATE player
                SET experience = {experience}
                WHERE player_id = {player_id}
                '''
        self.execute_query(query)

    def reset_player_fish_storage(self, player_id, commit=True):
        query = f'''UPDATE fish_stored
                SET stored_amount = 0
                FROM storage
                WHERE player_id = {player_id};
                '''
        self.execute_query(query, commit=commit)

    def get_fish_caught_id(self, player_id, fish_name):
        query = f'''SELECT fish_caught.id
                FROM fish_caught
                         JOIN public.stats s ON s.id = fish_caught.stats_id
                         JOIN player p ON s.player_id = p.player_id
                WHERE p.player_id = {player_id}
                  AND fish_name = '{fish_name}' '''
        return self.fetch_as_dicts(query)

    def update_fish_caught(self, fish_caught_id, amount):
        query = f'''UPDATE fish_caught
                SET caught_amount = {amount}
                WHERE id = {fish_caught_id}
                '''
        self.execute_query(query)

    def insert_player(self, player_id, player_username):
        query = f'''INSERT INTO player
                VALUES ({player_id}, '{player_username}', 0, 0, 0, 0);
                '''
        self.execute_query(query)

    def get_fish_stored_id(self, player_id, fish_name):
        query = f'''SELECT fish_stored.id
                FROM fish_stored
                         JOIN public.storage s ON s.id = fish_stored.storage_id
                         JOIN player p ON s.player_id = p.player_id
                WHERE p.player_id = {player_id}
                  AND fish_name = '{fish_name}' '''
        return self.fetch_as_dicts(query)

    def update_fish_stored(self, fish_stored_id, amount):
        query = f'''UPDATE fish_stored
                SET stored_amount = {amount}
                WHERE id = {fish_stored_id}
                '''
        self.execute_query(query)

    def update_balance(self, player_id, delta):
        query = f'''UPDATE stats
                SET balance = balance + {delta}
                WHERE player_id = {player_id}
                '''
        self.execute_query(query)

    def update_total_earning(self, player_id, delta):
        query = f'''UPDATE stats
                SET total_earning = total_earning + {delta}
                WHERE player_id = {player_id}
                '''
        self.execute_query(query)

    def update_player_rod_level(self, player_id, level):
        query = f'''UPDATE player
                SET rod_level = {level}
                WHERE player_id = {player_id}
                '''
        self.execute_query(query)

    def update_player_net_level(self, player_id, level):
        query = f'''UPDATE player
                SET net_level = {level}
                WHERE player_id = {player_id}
                '''
        self.execute_query(query)

    def sell_storage(self, player_id, delta):
        self.reset_player_fish_storage(player_id, commit=False)
        self.update_balance(player_id, delta)
        self.update_total_earning(player_id, delta)

    def up_player_rod(self, player_id, level, delta):
        self.update_player_rod_level(player_id, level)
        self.update_balance(player_id, delta)

    def up_player_net(self, player_id, level, delta):
        self.update_player_net_level(player_id, level)
        self.update_balance(player_id, delta)

    @staticmethod
    def open_connection():
        conn = None
        try:
            config = configparser.ConfigParser()
            config.read("settings/config.ini")
            conn = psycopg2.connect(dbname=config["Database"]["dbname"], user=config["Database"]["user"],
                                    password=config["Database"]["pass"], host=config["Database"]["hostname"],
                                    port=config["Database"]["port"])
        except Exception as e:
            print(f'Error: {e}')
        return conn

    @staticmethod
    def close_connection(conn):
        conn.close()
