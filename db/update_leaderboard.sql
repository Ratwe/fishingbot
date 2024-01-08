BEGIN;

UPDATE leaderboard AS l
SET rank = subquery.rank
FROM (
    SELECT player_id, total_earning, RANK() OVER (ORDER BY total_earning DESC) as rank
    FROM leaderboard
) AS subquery
WHERE l.player_id = subquery.player_id;

DO $$
BEGIN
    RAISE NOTICE 'Leaderboard was updated.';
END $$;

COMMIT;