CREATE OR REPLACE PROCEDURE update_leaderboard()
    LANGUAGE plpgsql
AS
$$
DECLARE
    current_time TIMESTAMP;
BEGIN
    current_time := NOW(); -- Get current timestamp

    UPDATE leaderboard AS l
    SET rank = subquery.rank
    FROM (SELECT player_id, total_earning, RANK() OVER (ORDER BY total_earning DESC) AS rank
          FROM leaderboard) AS subquery
    WHERE l.player_id = subquery.player_id;

    RAISE NOTICE 'Leaderboard was updated at %', current_time; -- Raise error message with current timestamp

END;
$$;

CALL update_leaderboard();