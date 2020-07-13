DROP TABLE IF EXISTS user;

CREATE TABLE user (
    id TEXT PRIMARY KEY UNIQUE NOT NULL,
    name TEXT,
    first_name TEXT,
    last_name TEXT,
    profile_pic TEXT,
    locale TEXT,
    timezone TEXT,
    gender TEXT DEFAULT "neutral"
);