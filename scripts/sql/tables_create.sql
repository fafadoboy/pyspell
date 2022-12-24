-- SQLite
CREATE TABLE words (
    id INTEGER NOT NULL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    audio_file BLOB NOT NULL
);

CREATE TABLE sets (
    id INTEGER NOT NULL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE set_words (
    set_id INTEGER REFERENCES sets,
    word_id INTEGER REFERENCES words
);

CREATE TABLE practices (
    id INTEGER NOT NULL PRIMARY KEY ASC,
    practice_set_id INTEGER,    
    success_ratio REAL,
    practice_date TEXT,
    wrong_words BLOB
);