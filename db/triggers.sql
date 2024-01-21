CREATE OR REPLACE FUNCTION insert_player()
    RETURNS TRIGGER AS
$$
DECLARE
    stats_id int;
    storage_id int;
BEGIN
    INSERT INTO leaderboard(player_id, rank)
    VALUES (NEW.player_id, NULL);

    INSERT INTO stats(player_id, balance, total_earning)
    VALUES (NEW.player_id, 0, 0)
    RETURNING id INTO stats_id;

    INSERT INTO fish_caught(stats_id, fish_name, caught_amount)
    VALUES (stats_id, 'cod', 0),
           (stats_id, 'salmon', 0),
           (stats_id, 'puffer', 0);

    INSERT INTO storage(player_id)
    VALUES (NEW.player_id)
    RETURNING id INTO storage_id;

    INSERT INTO fish_stored(storage_id, fish_name, stored_amount)
    VALUES (storage_id, 'cod', 0),
           (storage_id, 'salmon', 0),
           (storage_id, 'puffer', 0);

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER insert_player_trigger
    AFTER INSERT
    ON player
    FOR EACH ROW
EXECUTE FUNCTION insert_player();

CREATE OR REPLACE FUNCTION delete_player()
    RETURNS TRIGGER AS
$$
BEGIN
    DELETE FROM leaderboard
    WHERE player_id = OLD.player_id;

    DELETE FROM fish_caught
    WHERE stats_id IN (SELECT id FROM stats WHERE player_id = OLD.player_id);

    DELETE FROM stats
    WHERE player_id = OLD.player_id;

    DELETE FROM fish_stored
    WHERE storage_id IN (SELECT id FROM storage WHERE player_id = OLD.player_id);

    DELETE FROM storage
    WHERE player_id = OLD.player_id;

    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER delete_player_trigger
    BEFORE DELETE
    ON player
    FOR EACH ROW
EXECUTE FUNCTION delete_player();
