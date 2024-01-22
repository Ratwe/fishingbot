CREATE TABLE IF NOT EXISTS fish
(
    fish_name  VARCHAR(30) PRIMARY KEY,
    cost       INT,
    experience INT
);

DROP TABLE rod CASCADE;
CREATE TABLE IF NOT EXISTS rod
(
    level    INT PRIMARY KEY,
    price    DECIMAL(30, 0),
    cooldown FLOAT
);
CALL insert_rod(200);

DROP TABLE net CASCADE;
CREATE TABLE IF NOT EXISTS net
(
    level      INT PRIMARY KEY,
    price      DECIMAL(30, 0),
    cooldown   FLOAT,
    catch_coef FLOAT
);
CALL insert_net(200);

DROP TABLE player CASCADE;
CREATE TABLE IF NOT EXISTS player
(
    player_id  BIGINT PRIMARY KEY,
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
    player_id     BIGINT REFERENCES player (player_id) ON DELETE CASCADE,
    balance       INT,
    total_earning INT
);

CREATE TABLE IF NOT EXISTS fish_caught
(
    id            SERIAL PRIMARY KEY,
    stats_id      INT REFERENCES stats (id),
    fish_name     VARCHAR(30) REFERENCES fish (fish_name) ON DELETE CASCADE,
    caught_amount INT
);

CREATE TABLE IF NOT EXISTS storage
(
    id        SERIAL PRIMARY KEY,
    player_id BIGINT REFERENCES player (player_id) ON DELETE CASCADE
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
    player_id BIGINT REFERENCES player (player_id) ON DELETE CASCADE,
    rank      INT
);

CREATE TABLE IF NOT EXISTS promoted_channels
(
    id   SERIAL PRIMARY KEY,
    link VARCHAR(50) UNIQUE,
    taps INT
);


DROP TABLE level_hardness;
CREATE TABLE level_hardness
(
    level           INT PRIMARY KEY,
    rod_price       DECIMAL(30, 0),
    rod_time_to_buy FLOAT,
    rod_cooldown    FLOAT,
    net_price       DECIMAL(30, 0),
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

CREATE TABLE levels
(
    level        INT PRIMARY KEY,
    exp_required DECIMAL(20, 0)
);

drop table last_usages;
create table last_usages
(
    id serial PRIMARY KEY,
    player_id bigint REFERENCES player(player_id) on delete CASCADE,
    rod_last_use timestamp,
    net_last_use timestamp
);

INSERT INTO promoted_channels
VALUES (default, 'https://t.me/sobachki_real', 0),
       (default, 'https://t.me/kotiki_real', 0);

TRUNCATE TABLE player CASCADE;
INSERT INTO player
VALUES (2, 'name4', 0, 0, 2, 0),
       (3, 'name5', 0, 0, 1, 0),
       (4, 'name44', 0, 0, 1, 0);


insert into player VALUES (5128641039, 'dunda2', 0, 0, 1, 0);
delete from player where name = 'dunda2';

INSERT INTO fish(fish_name, cost, experience)
VALUES ('cod', 1, 3),
       ('salmon', 3, 5),
       ('puffer', 5, 10);

CALL insert_fish_chances(200);

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO dev;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO dev;