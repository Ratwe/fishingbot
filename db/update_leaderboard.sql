UPDATE leaderboard AS l
SET rank = subquery.rank, total_earning = earning
FROM (
    SELECT player_id, total_earning as earning, RANK() OVER (ORDER BY total_earning DESC) as rank
    FROM leaderboard
) AS subquery
WHERE l.player_id = subquery.player_id;