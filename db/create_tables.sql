CREATE TABLE IF NOT EXISTS fish
(
    fish_name  VARCHAR(30) PRIMARY KEY,
    cost       INT,
    experience INT
);


CREATE TABLE IF NOT EXISTS player
(
    player_id  INT PRIMARY KEY,
    name       VARCHAR(50),
    level      INT,
    experience INT,
    avg_catch  INT
);

CREATE TABLE IF NOT EXISTS rod
(
    id             SERIAL PRIMARY KEY,
    player_id      INT REFERENCES player (player_id) ON DELETE CASCADE,
    required_level INT,
    price          INT,
    cooldown       FLOAT
);

CREATE TABLE IF NOT EXISTS net
(
    id             SERIAL PRIMARY KEY,
    player_id      INT REFERENCES player (player_id) ON DELETE CASCADE,
    required_level INT,
    price          INT,
    cooldown       FLOAT
);

CREATE TABLE IF NOT EXISTS fish_chances
(
    id           SERIAL PRIMARY KEY,
    fish_name    VARCHAR(30) REFERENCES fish (fish_name) ON DELETE CASCADE,
    rod_level    INT REFERENCES rod (id) ON DELETE CASCADE,
    net_level    INT REFERENCES net (id) ON DELETE CASCADE,
    catch_chance NUMERIC(3, 3)
);


CREATE TABLE IF NOT EXISTS stats
(
    id            SERIAL PRIMARY KEY,
    player_id     INT REFERENCES player (player_id) ON DELETE CASCADE,
    balance       INT,
    total_earning INT
);

CREATE TABLE IF NOT EXISTS fish_caught
(
    id            SERIAL PRIMARY KEY,
    stats_id      INT REFERENCES stats (id),
    fish_name     VARCHAR(30) REFERENCES fish (fish_name),
    caught_amount INT
);

CREATE TABLE IF NOT EXISTS storage
(
    id        SERIAL PRIMARY KEY,
    player_id INT REFERENCES player (player_id)
);

CREATE TABLE IF NOT EXISTS fish_stored
(
    id            SERIAL PRIMARY KEY,
    storage_id    INT REFERENCES storage (id),
    fish_name     VARCHAR(30) REFERENCES fish (fish_name),
    stored_amount INT
);

CREATE TABLE IF NOT EXISTS leaderboard
(
    id        SERIAL PRIMARY KEY,
    player_id INT REFERENCES player (player_id),
    rank      INT
);

INSERT INTO player
VALUES (2, 'name2', 0, 0, 2);

insert into fish(fish_name, cost, experience) VALUES
                                                  ('cod', 1, 3),
                                                  ('salmon', 3, 5),
                                                  ('puffer', 5, 10);
