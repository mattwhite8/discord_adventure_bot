-- core game world structure
CREATE TABLE IF NOT EXISTS Rooms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    short_description TEXT
);

-- player identity management
CREATE TABLE IF NOT EXISTS Characters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    discord_user_id TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- flexible character state management
CREATE TABLE IF NOT EXISTS CharacterStates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    character_id INTEGER NOT NULL,
    current_room_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (character_id) REFERENCES Characters(id),
    FOREIGN KEY (current_room_id) REFERENCES Rooms(id)
);

-- room connectivity for navigation
CREATE TABLE IF NOT EXISTS RoomConnections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    from_room_id INTEGER NOT NULL,
    to_room_id INTEGER NOT NULL,
    direction TEXT NOT NULL,
    FOREIGN KEY (from_room_id) REFERENCES Rooms(id),
    FOREIGN KEY (to_room_id) REFERENCES Rooms(id)
);

CREATE INDEX idx_characters_discord_id ON Characters(discord_user_id);
CREATE INDEX idx_character_states_character_id ON CharacterStates(character_id);
CREATE INDEX idx_character_states_current_room ON CharacterStates(current_room_id);
CREATE INDEX idx_room_connections_from ON RoomConnections(from_room_id);

CREATE UNIQUE INDEX idx_character_states_unique_character ON CharacterStates(character_id);
