CREATE OR REPLACE PROCEDURE insert_fishing_chances(count INT)
    LANGUAGE plpgsql
AS
$$
DECLARE
    i INT;
    current_rod_level INT;
    current_net_level INT;
    cod_chance NUMERIC(4, 3);
    salmon_chance NUMERIC(4, 3);
    puffer_chance NUMERIC(4, 3);
BEGIN
    FOR i IN 0..count LOOP
        current_rod_level := i;
        current_net_level := i;

        IF i <= 5 THEN
            cod_chance := 1.0;
            salmon_chance := 0.0;
            puffer_chance := 0.0;
        ELSIF i <= 9 THEN
            cod_chance := GREATEST(0.0, 1.0 - 0.15 * (i - 5));
            salmon_chance := LEAST(1.0, 0.15 * (i - 5));
            puffer_chance := 0.0;
        ELSIF i = 10 THEN
            cod_chance := 0.20;
            salmon_chance := 0.75;
            puffer_chance := 0.05;
        ELSE
            cod_chance := GREATEST(0.0000, cod_chance * 0.8);
            salmon_chance := GREATEST(0.0000, salmon_chance * 0.9);
            puffer_chance := 1.0 - cod_chance - salmon_chance;
        END IF;

        INSERT INTO fish_chances (fish_name, rod_level, net_level, catch_chance)
        VALUES ('cod', current_rod_level, current_net_level, cod_chance),
               ('salmon', current_rod_level, current_net_level, salmon_chance),
               ('puffer', current_rod_level, current_net_level, puffer_chance);
    END LOOP;
END;
$$;

TRUNCATE fish_chances;
call insert_fishing_chances(50);
select * from fish_chances;