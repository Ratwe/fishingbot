CREATE OR REPLACE PROCEDURE insert_rod(start INT, finish int)
    LANGUAGE plpgsql
AS
$$
DECLARE
    i INT;
    current_price DECIMAL(1000,0);
    current_cooldown FLOAT;
BEGIN
    FOR i IN start..finish LOOP
        current_price := 20 * (1.15)^(i - 1);
        current_cooldown := 20 * (0.97)^(i);

        INSERT INTO rod (level, price, cooldown)
        VALUES (i, current_price, current_cooldown);
    END LOOP;
END;
$$;

CREATE OR REPLACE PROCEDURE update_rod(start INT, finish INT)
    LANGUAGE plpgsql
AS
$$
DECLARE
    i                  INT;
    current_price      DECIMAL (1000, 0);
    current_cooldown   FLOAT;
BEGIN
    FOR i IN start..finish
        LOOP
            current_price := 20 * (1.15)^(i - 1);
            current_cooldown := 20 * (0.97)^(i);

            UPDATE rod
            set cooldown = current_cooldown
            where level = i;
        END LOOP;
END;
$$;


TRUNCATE table rod CASCADE;
call insert_rod(201, 1000);
call update_rod(201, 1000);
alter table rod alter column price type DECIMAL (1000, 0);
select * from rod;