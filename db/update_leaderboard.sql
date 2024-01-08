CREATE OR REPLACE PROCEDURE update_leaderboard()
    LANGUAGE plpgsql
AS
$$
BEGIN

    UPDATE leaderboard AS l
    SET rank = subquery.rank
    FROM (SELECT player_id, total_earning, RANK() OVER (ORDER BY total_earning DESC) AS rank
          FROM leaderboard) AS subquery
    WHERE l.player_id = subquery.player_id;

    RAISE NOTICE 'Leaderboard was updated.';

END;
$$;

CALL update_leaderboard();