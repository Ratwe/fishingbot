CREATE OR REPLACE PROCEDURE insert_rod(count INT)
    LANGUAGE plpgsql
AS
$$
DECLARE
    i INT;
    current_price DECIMAL(30,0);
    current_cooldown FLOAT;
BEGIN
    FOR i IN 0..count LOOP
        current_price := 20 * (1.15)^(i - 1);
        current_cooldown := 20 * (0.97)^(i);

        INSERT INTO rod (level, price, cooldown)
        VALUES (i, current_price, current_cooldown);
    END LOOP;
END;
$$;

TRUNCATE table rod CASCADE;
call insert_rod(200);
select * from rod;