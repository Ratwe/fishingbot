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

CREATE TABLE players
(
    player_id INT PRIMARY KEY,
    rod       INT REFERENCES rod (level),
    net       BOOL REFERENCES net (purchased)
);

CREATE TABLE storage
(
    player_id       INT REFERENCES players (player_id),
    cod_storaged    INT,
    salmon_storaged INT,
    puffer_storaged INT
);

CREATE TABLE stats
(
    player_id     INT REFERENCES players (player_id),
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
    fish_id    INT PRIMARY KEY,
    cost       INT,
    experience INT
);