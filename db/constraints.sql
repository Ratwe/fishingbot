ALTER TABLE fish
ADD CHECK (cost >= 0);
ALTER TABLE fish
ADD CHECK (experience >= 0);
ALTER TABLE fish
ALTER COLUMN fish_name SET NOT NULL;

ALTER TABLE rod
ADD CHECK (price >= 0);
ALTER TABLE rod
ADD CHECK (cooldown >= 0);
ALTER TABLE rod
ALTER COLUMN level SET NOT NULL;

ALTER TABLE net
ADD CHECK (price >= 0);
ALTER TABLE net
ADD CHECK (cooldown >= 0);
ALTER TABLE net
ADD CHECK (catch_coef >= 0);
ALTER TABLE net
ALTER COLUMN level SET NOT NULL;

ALTER TABLE player
ADD CHECK (level >= 0);
ALTER TABLE player
ADD CHECK (experience >= 0);
ALTER TABLE player
ALTER COLUMN player_id SET NOT NULL;

ALTER TABLE fish_chances
ADD CHECK (catch_chance >= 0);

ALTER TABLE stats
ADD CHECK (balance >= 0);
ALTER TABLE stats
ADD CHECK (total_earning  >= 0);

ALTER TABLE fish_caught
ADD CHECK (caught_amount >= 0);

ALTER TABLE fish_stored
ADD CHECK (stored_amount >= 0);

ALTER TABLE leaderboard
ADD CHECK (rank > 0);

ALTER TABLE levels
ADD CHECK (exp_required >= 0);
ALTER TABLE levels
ADD CHECK (level >= 0);

ALTER TABLE promoted_channels
ADD CHECK (taps >= 0);

ALTER TABLE utm
ADD CHECK (clicks >= 0);
