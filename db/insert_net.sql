CREATE OR REPLACE PROCEDURE insert_net(count INT)
    LANGUAGE plpgsql
AS
$$
DECLARE
    i                  INT;
    current_price      DECIMAL(30, 0);
    current_cooldown   FLOAT;
    current_catch_coef FLOAT;
BEGIN
    FOR i IN 0..count
        LOOP
            current_price := 600 * (1.15) ^ (i - 9) * 3;
            current_cooldown := 300;
            current_catch_coef := 10 + i;

            INSERT INTO net (level, price, cooldown, catch_coef)
            VALUES (i, current_price, current_cooldown, current_catch_coef);
        END LOOP;
END;
$$;

TRUNCATE TABLE net CASCADE;
CALL insert_net(200);
select * from net;
