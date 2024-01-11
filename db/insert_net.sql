CREATE OR REPLACE PROCEDURE insert_net(count INT)
    LANGUAGE plpgsql
AS
$$
DECLARE
    i                  INT;
    current_price      INT;
    current_cooldown   FLOAT;
    current_catch_coef FLOAT;
BEGIN
    FOR i IN 0..count
        LOOP
            current_price := 150 * (1.2) ^ (i - 9) * 3;
            current_cooldown := 100;
            current_catch_coef := 1 + (i) * 0.1;

            INSERT INTO net (level, price, cooldown, catch_coef)
            VALUES (i, current_price, current_cooldown, current_catch_coef);
        END LOOP;
END;
$$;

TRUNCATE TABLE net CASCADE;
CALL insert_net(50);
select * from net;
