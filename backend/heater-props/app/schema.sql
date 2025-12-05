-- Picks table for active/upcoming picks
CREATE TABLE IF NOT EXISTS picks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    player_name TEXT NOT NULL,
    prop_type TEXT NOT NULL, -- 'points', 'rebounds', 'assists'
    line REAL NOT NULL,
    prediction TEXT NOT NULL, -- 'over' or 'under'
    game_id TEXT NOT NULL,
    home_team TEXT NOT NULL,
    away_team TEXT NOT NULL,
    game_date TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id),
    UNIQUE(user_id, player_name, prop_type, game_id) -- Prevent duplicate picks
);

-- Pick history for completed games
CREATE TABLE IF NOT EXISTS pick_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    player_name TEXT NOT NULL,
    prop_type TEXT NOT NULL,
    line REAL NOT NULL,
    prediction TEXT NOT NULL,
    game_id TEXT NOT NULL,
    home_team TEXT NOT NULL,
    away_team TEXT NOT NULL,
    game_date TIMESTAMP NOT NULL,
    actual_result REAL, -- actual stat value
    result TEXT, -- 'win', 'loss', 'push'
    created_at TIMESTAMP,
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- User statistics
CREATE TABLE IF NOT EXISTS user_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE NOT NULL,
    total_picks INTEGER DEFAULT 0,
    wins INTEGER DEFAULT 0,
    losses INTEGER DEFAULT 0,
    pushes INTEGER DEFAULT 0,
    points_picks INTEGER DEFAULT 0,
    points_wins INTEGER DEFAULT 0,
    rebounds_picks INTEGER DEFAULT 0,
    rebounds_wins INTEGER DEFAULT 0,
    assists_picks INTEGER DEFAULT 0,
    assists_wins INTEGER DEFAULT 0,
    current_streak INTEGER DEFAULT 0,
    best_streak INTEGER DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_picks_user_id ON picks(user_id);
CREATE INDEX IF NOT EXISTS idx_picks_game_date ON picks(game_date);
CREATE INDEX IF NOT EXISTS idx_pick_history_user_id ON pick_history(user_id);
CREATE INDEX IF NOT EXISTS idx_pick_history_game_date ON pick_history(game_date);
CREATE INDEX IF NOT EXISTS idx_pick_history_result ON pick_history(result);
