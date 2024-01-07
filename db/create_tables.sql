CREATE TABLE rod
(
    level         INT PRIMARY KEY,
    cod_chance    FLOAT,
    salmon_chance FLOAT,
    puffer_chance FLOAT,
    min_catch     INT,
    max_catch     INT
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
    level         INT,
    experience    INT,
    balance       INT,
    total_earning INT,
    cod_caught    INT,
    salmon_caught INT,
    puffer_caught INT
);

CREATE TABLE fish
(
    name  TEXT PRIMARY KEY,
    cost       INT,
    experience INT
);
