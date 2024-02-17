CREATE OR REPLACE PROCEDURE insert_fish_chances(count INT)
    LANGUAGE plpgsql
AS
$$
DECLARE
    i                 INT;
    current_rod_level INT;
    current_net_level INT;
    old_fish_id       INT = -2;
    mid_fish_id       INT = -1;
    new_fish_id       INT = 0;
    old_fish_chance   NUMERIC(4, 3);
    mid_fish_chance   NUMERIC(4, 3);
    new_fish_chance   NUMERIC(4, 3);
    fish_types        INT;
BEGIN
    SELECT COUNT(*) INTO fish_types FROM fish;

    FOR i IN 0..count
        LOOP
            current_rod_level := i;
            current_net_level := i;

            IF i % 5 = 0 AND (i / 5 + 1) <= fish_types THEN
                old_fish_id := old_fish_id + 1;
                mid_fish_id := mid_fish_id + 1;
                new_fish_id := new_fish_id + 1;

                IF i >= 10 THEN
                    old_fish_chance = 0.2;
                    mid_fish_chance = 0.75;
                    new_fish_chance = 0.05;
                END IF;
            ELSE
                IF i < 5 THEN
                    old_fish_chance := 0.0;
                    mid_fish_chance := 0.0;
                    new_fish_chance := 1.0;
                ELSIF i < 10 THEN
                    old_fish_chance := 0;
                    mid_fish_chance := 1.0 - 0.15 * (i - 4);
                    new_fish_chance := 0.15 * (i - 4);
                ELSE
                    old_fish_chance := GREATEST(0.0000, old_fish_chance * 0.8);
                    mid_fish_chance := GREATEST(0.0000, mid_fish_chance * 0.9);
                    new_fish_chance := 1.0 - old_fish_chance - mid_fish_chance;
                END IF;
            END IF;

            IF (i < 5) THEN
                INSERT INTO fish_chances (fish_id, rod_level, net_level, catch_chance)
                VALUES (new_fish_id, current_rod_level, current_net_level, new_fish_chance);
            ELSIF (i < 10) THEN
                INSERT INTO fish_chances (fish_id, rod_level, net_level, catch_chance)
                VALUES (new_fish_id, current_rod_level, current_net_level, new_fish_chance),
                       (mid_fish_id, current_rod_level, current_net_level, mid_fish_chance);
            ELSE
                INSERT INTO fish_chances (fish_id, rod_level, net_level, catch_chance)
                VALUES (new_fish_id, current_rod_level, current_net_level, new_fish_chance),
                       (mid_fish_id, current_rod_level, current_net_level, mid_fish_chance),
                       (old_fish_id, current_rod_level, current_net_level, old_fish_chance);

            END IF;
        END LOOP;
END;
$$;

--TRUNCATE fish_chances;
TRUNCATE fish_chances;
CALL insert_fish_chances(200);
SELECT *
FROM fish_chances_new;