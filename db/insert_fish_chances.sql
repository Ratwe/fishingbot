CREATE OR REPLACE PROCEDURE insert_fishing_chances(count INT)
    LANGUAGE plpgsql
AS
$$
DECLARE
    i INT;
    current_rod_id INT;
    current_net_id INT;
    cod_chance NUMERIC(4, 3);
    salmon_chance NUMERIC(4, 3);
    puffer_chance NUMERIC(4, 3);
BEGIN
    FOR i IN 0..count LOOP
        select id from rod where required_level = i into current_rod_id;
        select id from net where required_level = i + 5 into current_net_id;

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

        INSERT INTO fish_chances (fish_name, rod_id, net_id, catch_chance)
        VALUES ('cod', current_rod_id, current_net_id, cod_chance),
               ('salmon', current_rod_id, current_net_id, salmon_chance),
               ('puffer', current_rod_id, current_net_id, puffer_chance);
    END LOOP;
END;
$$;

TRUNCATE fish_chances;
call insert_fishing_chances(50);