CREATE OR REPLACE PROCEDURE calc_level_hardness(count INT)
    LANGUAGE plpgsql
AS
$$
DECLARE
    i               INT;
    rod_price       DECIMAL(30, 0);
    net_price       DECIMAL(30, 0);
    rod_cooldown    FLOAT;
    net_cooldown    FLOAT;
    net_catch_coef  FLOAT;
    avg_catch       INT;
    total_rod_cost  FLOAT := 0; -- Initialize to 0
    total_rod_exp   FLOAT := 0; -- Initialize to 0
    total_net_cost  FLOAT := 0; -- Initialize to 0
    total_net_exp   FLOAT := 0; -- Initialize to 0
    avg_rod_cost    FLOAT;
    avg_rod_exp     FLOAT;
    avg_net_cost    FLOAT;
    avg_net_exp     FLOAT;
    cost_per_second FLOAT;
    exp_per_second  FLOAT;
    fish_data       fish_data_type[]; -- Declare as an array of records
    cur_fish_data   fish_data_type;
    cur_cost        FLOAT;
    cur_exp         FLOAT;
    exp_to_unlock   FLOAT;
    new_level_time  FLOAT;
    rod_time_to_buy FLOAT;
    net_time_to_buy FLOAT;
BEGIN
    TRUNCATE level_hardness;
    TRUNCATE levels;

    FOR i IN 1..count
        LOOP
            rod_price := 20 * (1.15) ^ (i - 1);
            rod_cooldown := 5 * (0.97) ^ i; -- Adjusted the exponent
            net_price := 150 * (1.15) ^ (i - 9) * 3;
            net_cooldown := 100;
            net_catch_coef := 1 + i * 0.1;

            avg_catch := 5 + i - 1;

            SELECT ARRAY_AGG(ROW (fish.fish_name, fish_chances.catch_chance))
            INTO fish_data
            FROM fish_chances
                     JOIN net ON net.level = fish_chances.net_level
                     JOIN fish ON fish_chances.fish_name = fish.fish_name
            WHERE net.level = i;

            total_rod_cost := 0;
            total_rod_exp := 0;
            total_net_cost := 0;
            total_net_exp := 0;

            FOREACH cur_fish_data IN ARRAY fish_data
                LOOP
                    SELECT cost, experience
                    INTO cur_cost, cur_exp
                    FROM fish
                    WHERE fish_name = cur_fish_data.fish_name;

                    total_rod_cost := total_rod_cost + cur_cost * avg_catch * cur_fish_data.catch_chance;
                    total_rod_exp := total_rod_exp + cur_exp * avg_catch * cur_fish_data.catch_chance;
                    total_net_cost :=
                                total_net_cost + cur_cost * avg_catch * cur_fish_data.catch_chance * net_catch_coef;
                    total_net_exp := total_net_exp + cur_exp * avg_catch * cur_fish_data.catch_chance * net_catch_coef;
                END LOOP;

            avg_rod_cost := total_rod_cost / rod_cooldown;
            avg_rod_exp := total_rod_exp / rod_cooldown;
            avg_net_cost := total_net_cost / net_cooldown;
            avg_net_exp := total_net_exp / net_cooldown;
            cost_per_second := avg_rod_cost + avg_net_cost;
            exp_per_second := avg_rod_exp + avg_net_exp;

            new_level_time := 20 * 1.05 ^ (i - 1);
            exp_to_unlock = new_level_time * exp_per_second;

            rod_time_to_buy = rod_price / cost_per_second;
            net_time_to_buy = net_price / cost_per_second;


            INSERT INTO level_hardness
            VALUES (i, rod_price, rod_time_to_buy, rod_cooldown, net_price, net_time_to_buy, net_cooldown,
                    net_catch_coef, avg_rod_cost, avg_rod_exp,
                    avg_net_cost, avg_net_exp, cost_per_second, exp_per_second, exp_to_unlock, new_level_time);

            INSERT INTO levels VALUES (i, exp_to_unlock);
        END LOOP;

END;
$$;

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


TRUNCATE level_hardness;
CALL calc_level_hardness(200);
SELECT level, rod_price, rod_time_to_buy, net_price, net_time_to_buy, cost_per_second, time_to_unlock
FROM level_hardness;
