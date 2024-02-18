CREATE OR REPLACE PROCEDURE insert_net(start INT, finish INT)
    LANGUAGE plpgsql
AS
$$
DECLARE
    i                  INT;
    current_price      DECIMAL(100, 0);
    current_cooldown   FLOAT;
    current_catch_coef FLOAT;
BEGIN
    FOR i IN start..finish
        LOOP
            current_price := 600 * (1.15) ^ (i - 9) * 3;
            current_cooldown := 300;
            current_catch_coef := 10 + i;

            INSERT INTO net (level, price, cooldown, catch_coef)
            VALUES (i, current_price, current_cooldown, current_catch_coef);
        END LOOP;
END;
$$;

CREATE OR REPLACE PROCEDURE update_net(start INT, finish INT)
    LANGUAGE plpgsql
AS
$$
DECLARE
    i                  INT;
    current_price      DECIMAL (1000, 0);
    current_cooldown   FLOAT;
    current_catch_coef FLOAT;
BEGIN
    FOR i IN start..finish
        LOOP
            current_price := 600 * (1.15) ^ (i - 9) * 3;
            current_cooldown := 300;
            current_catch_coef := 10 + i;

            UPDATE net
            set cooldown = current_cooldown
            where level = i;
        END LOOP;
END;
$$;

TRUNCATE  NET;
CALL insert_net(201, 1000);
CALL update_net(201, 1000);
select * from net;

alter table net alter column price type DECIMAL (1000, 0);