CREATE TABLE rod
(
    level         INT PRIMARY KEY,
    price         INT,
    cod_chance    FLOAT,
    salmon_chance FLOAT,
    puffer_chance FLOAT,
    min_catch     INT,
    max_catch     INT,
    cooldown      FLOAT
);

CREATE TABLE net
(
    purchased     bool PRIMARY KEY,
    cod_chance    FLOAT,
    salmon_chance FLOAT,
    puffer_chance FLOAT,
    min_catch     INT,
    max_catch     INT,
    cooldown      INT
);

CREATE TABLE player
(
    player_id INT PRIMARY KEY,
    rod       INT REFERENCES rod (level),
    net       BOOL REFERENCES net (purchased)
);

CREATE TABLE storage
(
    player_id     INT REFERENCES player (player_id),
    cod_stored    INT,
    salmon_stored INT,
    puffer_stored INT
);

CREATE TABLE stats
(
    player_id     INT REFERENCES player (player_id),
    balance       INT,
    total_earning INT,
    cod_caught    INT,
    salmon_caught INT,
    puffer_caught INT,
    rank int REFERENCES leaderboard(player_id)
);

CREATE TABLE fish
(
    name TEXT PRIMARY KEY,
    cost INT
);

CREATE TABLE leaderboard
(
    player_id int unique REFERENCES player(player_id),
    total_earning int,
    rank int
);

INSERT INTO leaderboard
(player_id, total_earning, rank)
VALUES
((SELECT player_id FROM player ORDER BY random() LIMIT 1),
 FLOOR(random() * 1000),
 null);

INSERT INTO player
(player_id, rod, net)
VALUES
(FLOOR(random() * 100), -- player_id
 FLOOR(random() * 10), -- rod
 CASE WHEN random() > 0.5 THEN TRUE ELSE FALSE END); -- net

