CREATE OR REPLACE PROCEDURE insert_net(count INT)
    LANGUAGE plpgsql
AS
$$
DECLARE
    i                INT;
    current_price    INT;
    current_cooldown FLOAT;
BEGIN
    FOR i IN 10..count
        LOOP
            current_price := 150 * (1.2) ^ (i - 9) * 3;
            current_cooldown := 100;

            INSERT INTO net (required_level, price, cooldown)
            VALUES (i, current_price, current_cooldown);
        END LOOP;
END;
$$;

TRUNCATE TABLE net CASCADE;
CALL insert_net(50);
