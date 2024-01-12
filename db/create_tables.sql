CREATE TABLE IF NOT EXISTS fish
(
    fish_name  VARCHAR(30) PRIMARY KEY,
    cost       INT,
    experience INT
);

DROP TABLE rod;
CREATE TABLE IF NOT EXISTS rod
(
    level    INT PRIMARY KEY,
    price    INT,
    cooldown FLOAT
);

DROP TABLE net;
CREATE TABLE IF NOT EXISTS net
(
    level      INT PRIMARY KEY,
    price      INT,
    cooldown   FLOAT,
    catch_coef FLOAT
);

DROP TABLE player CASCADE;
CREATE TABLE IF NOT EXISTS player
(
    player_id  INT PRIMARY KEY,
    name       VARCHAR(50),
    rod_level  INT REFERENCES rod (level),
    net_level  INT REFERENCES net (level),
    level      INT,
    experience INT
);


DROP TABLE fish_chances;
CREATE TABLE IF NOT EXISTS fish_chances
(
    id           SERIAL PRIMARY KEY,
    fish_name    VARCHAR(30) REFERENCES fish (fish_name) ON DELETE CASCADE,
    rod_level    INT REFERENCES rod (level),
    net_level    INT REFERENCES net (level),
    catch_chance NUMERIC(4, 3)
);

CREATE TABLE IF NOT EXISTS stats
(
    id            SERIAL PRIMARY KEY,
    player_id     INT REFERENCES player (player_id) ON DELETE CASCADE,
    balance       INT,
    total_earning INT
);

delete from player where player_id = 2;

CREATE TABLE IF NOT EXISTS fish_caught
(
    id            SERIAL PRIMARY KEY,
    stats_id      INT REFERENCES stats (id),
    fish_name     VARCHAR(30) REFERENCES fish (fish_name)  ON DELETE CASCADE,
    caught_amount INT
);

CREATE TABLE IF NOT EXISTS storage
(
    id        SERIAL PRIMARY KEY,
    player_id INT REFERENCES player (player_id)  ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS fish_stored
(
    id            SERIAL PRIMARY KEY,
    storage_id    INT REFERENCES storage (id),
    fish_name     VARCHAR(30) REFERENCES fish (fish_name) ON DELETE CASCADE,
    stored_amount INT
);

DROP TABLE leaderboard;
CREATE TABLE IF NOT EXISTS leaderboard
(
    id        SERIAL PRIMARY KEY,
    player_id INT REFERENCES player (player_id) ON DELETE CASCADE,
    rank      INT
);

CREATE TABLE IF NOT EXISTS promote_channels
(
    id   SERIAL PRIMARY KEY,
    link VARCHAR(50) UNIQUE,
    taps INT
);

INSERT INTO promote_channels
VALUES (default, 'https://t.me/sobachki_real', 0),
       (default, 'https://t.me/kotiki_real', 0);

TRUNCATE TABLE player CASCADE;
INSERT INTO player
VALUES (2, 'name2', 0, 0, 2, 0),
       (3, 'name3', 0, 0, 1, 0);

INSERT INTO fish(fish_name, cost, experience)
VALUES ('cod', 1, 3),
       ('salmon', 3, 5),
       ('puffer', 5, 10);
