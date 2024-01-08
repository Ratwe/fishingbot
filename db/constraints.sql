ALTER TABLE rod
    ADD CONSTRAINT non_less_zero_catch_chance
        CHECK ( cod_chance * salmon_chance * puffer_chance >= 0 );

ALTER TABLE rod
    ADD CONSTRAINT non_zero_min_catch
        CHECK ( min_catch > 0);

ALTER TABLE net
    ADD CONSTRAINT non_less_zero_catch_chance
        CHECK ( cod_chance * salmon_chance * puffer_chance >= 0 );

ALTER TABLE net
    ADD CONSTRAINT non_zero_min_catch
        CHECK ( min_catch > 0);

ALTER TABLE net
    ADD CONSTRAINT non_zero_cooldown
        CHECK ( cooldown > 0 );

ALTER TABLE storage
    ADD CONSTRAINT non_less_zero_cod_stored
        CHECK (cod_stored >= 0);

ALTER TABLE storage
    ADD CONSTRAINT non_less_zero_salmon_stored
        CHECK (salmon_stored >= 0);

ALTER TABLE storage
    ADD CONSTRAINT non_less_zero_puffer_stored
        CHECK (puffer_stored >= 0);

ALTER TABLE stats
    ADD CONSTRAINT non_less_zero_balance
        CHECK ( balance >= 0);

ALTER TABLE stats
    ADD CONSTRAINT non_less_zero_total_earning
        CHECK ( total_earning >= 0);

ALTER TABLE stats
    ADD CONSTRAINT non_less_zero_cod_caught
        CHECK ( cod_caught >= 0);

ALTER TABLE stats
    ADD CONSTRAINT non_less_zero_salmon_caught
        CHECK ( salmon_caught >= 0);

ALTER TABLE stats
    ADD CONSTRAINT non_less_zero_puffer_caught
        CHECK ( puffer_caught >= 0);

ALTER TABLE fish
    ADD CONSTRAINT non_zero_cost
        CHECK ( cost > 0 );

ALTER TABLE leaderboard
    ADD CONSTRAINT non_zero_rank
        CHECK ( rank > 0 );

ALTER TABLE leaderboard
    ADD CONSTRAINT non_less_zero_earning
        CHECK ( total_earning >= 0 );


SELECT con.*
FROM pg_catalog.pg_constraint con
     INNER JOIN pg_catalog.pg_class rel ON rel.oid = con.conrelid
     INNER JOIN pg_catalog.pg_namespace nsp ON nsp.oid = connamespace
WHERE nsp.nspname = 'public'
      AND rel.relname = 'stats';
