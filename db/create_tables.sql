CREATE TABLE IF NOT EXISTS fish
(
    id         INT PRIMARY KEY,
    fish_name  VARCHAR(30),
    cost       INT,
    experience INT
);

CREATE TABLE IF NOT EXISTS rod
(
    level    INT PRIMARY KEY,
    price    DECIMAL(1000, 0),
    cooldown FLOAT
);
CALL insert_rod(200);

CREATE TABLE IF NOT EXISTS net
(
    level      INT PRIMARY KEY,
    price      DECIMAL(1000, 0),
    cooldown   FLOAT,
    catch_coef FLOAT
);
CALL insert_net(200);

CREATE TABLE IF NOT EXISTS player
(
    player_id  BIGINT PRIMARY KEY,
    name       VARCHAR(50),
    rod_level  INT REFERENCES rod (level),
    net_level  INT REFERENCES net (level),
    level      INT,
    experience INT
);

CREATE TABLE IF NOT EXISTS fish_chances
(
    id           SERIAL PRIMARY KEY,
    fish_id      INT REFERENCES fish (id)
        ON DELETE CASCADE,
    rod_level    INT REFERENCES rod (level),
    net_level    INT REFERENCES net (level),
    catch_chance NUMERIC(4, 3)
);
CALL insert_fish_chances(200);

CREATE TABLE IF NOT EXISTS stats
(
    id            SERIAL PRIMARY KEY,
    player_id     BIGINT REFERENCES player (player_id)
        ON DELETE CASCADE,
    balance       BIGINT,
    total_earning BIGINT
);

CREATE TABLE IF NOT EXISTS fish_caught
(
    id            SERIAL PRIMARY KEY,
    stats_id      INT REFERENCES stats (id),
    fish_id       INT REFERENCES fish (id)
        ON DELETE CASCADE,
    caught_amount INT
);

CREATE TABLE IF NOT EXISTS storage
(
    id        SERIAL PRIMARY KEY,
    player_id BIGINT REFERENCES player (player_id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS fish_stored
(
    id            SERIAL PRIMARY KEY,
    storage_id    INT REFERENCES storage (id),
    fish_id       INT REFERENCES fish (id)
        ON DELETE CASCADE,
    stored_amount INT
);

CREATE TABLE IF NOT EXISTS leaderboard
(
    id        SERIAL PRIMARY KEY,
    player_id BIGINT REFERENCES player (player_id)
        ON DELETE CASCADE,
    rank      INT
);

CREATE TABLE IF NOT EXISTS level_hardness
(
    level           INT PRIMARY KEY,
    rod_price       DECIMAL(1000, 0),
    rod_time_to_buy FLOAT,
    rod_cooldown    FLOAT,
    net_price       DECIMAL(1000, 0),
    net_time_to_buy FLOAT,
    net_cooldown    FLOAT,
    net_catch_coef  FLOAT,
    avg_rod_cost    FLOAT,
    avg_rod_exp     FLOAT,
    avg_net_cost    FLOAT,
    avg_net_exp     FLOAT,
    cost_per_second FLOAT,
    exp_per_second  FLOAT,
    exp_to_unlock   DECIMAL(20, 0),
    time_to_unlock  FLOAT
);
CALL calc_level_hardness(50);

CREATE TABLE IF NOT EXISTS levels
(
    level        INT PRIMARY KEY,
    exp_required DECIMAL(20, 0)
);

CREATE TABLE IF NOT EXISTS last_usages
(
    id           SERIAL PRIMARY KEY,
    player_id    BIGINT REFERENCES player (player_id)
        ON DELETE CASCADE,
    rod_last_use TIMESTAMP,
    net_last_use TIMESTAMP
);

CREATE TABLE IF NOT EXISTS promoted_channels
(
    id   SERIAL PRIMARY KEY,
    link VARCHAR(50) UNIQUE,
    taps INT
);

CREATE TABLE IF NOT EXISTS utm
(
    id    SERIAL PRIMARY KEY,
    name  VARCHAR(50),
    clicks INT
);