from app.database.db_connector import get_db_connection

CHARACTER_NAME = "The Adventurer"
CHARACTER_ID = "MAIN_CHARACTER"
STARTER_ROOM = "Entrance Hall"


# TODO: Make this more reuseable, insert name and id
def get_or_create_character():
    with get_db_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT c.id, c.name
            FROM Characters c
            WHERE c.discord_user_id = ?
        """,
            (CHARACTER_ID,),
        )

        character = cursor.fetchone()

        if not character:
            cursor.execute(
                """
                INSERT INTO Characters (discord_user_id, name) VALUES (?, ?);
            """,
                (CHARACTER_ID, CHARACTER_NAME),
            )
            character_id = cursor.lastrowid
            character_name = CHARACTER_NAME
        else:
            character_id = character[0]
            character_name = character[1]

        cursor.execute(
            """
            SELECT id FROM Rooms WHERE name = ?
        """,
            (STARTER_ROOM,),
        )
        starter_room_id = cursor.fetchone()

        if not starter_room_id:
            raise Exception(f"Starter room '{STARTER_ROOM}' not found in database.")

        # Delete row with character_id from CharacterStates
        cursor.execute(
            """
            DELETE FROM CharacterStates WHERE character_id = ?
        """,
            (character_id,),
        )

        # Insert new character state
        cursor.execute(
            """
            INSERT INTO CharacterStates (character_id, current_room_id) VALUES (?, ?)
        """,
            (character_id, starter_room_id[0]),
        )

        conn.commit()

        return character_name


def get_character_status():
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Get current room and room description
        cursor.execute(
            """
            SELECT Rooms.name, Rooms.description
            FROM Rooms
            JOIN CharacterStates ON Rooms.id = CharacterStates.current_room_id
            JOIN Characters ON CharacterStates.character_id = Characters.id
            WHERE Characters.discord_user_id = ?;
        """,
            (CHARACTER_ID,),
        )

        room = cursor.fetchone()

        if not room:
            return "Unknown", "No character found, use /begin_adventure to start!"

    return room[0], room[1]


def get_room_exits():
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Get current room
        cursor.execute(
            """
            SELECT r.name, r.description
            FROM Rooms r
            JOIN CharacterStates ON r.id = CharacterStates.current_room_id
            JOIN Characters ON CharacterStates.character_id = Characters.id
            WHERE Characters.discord_user_id = ?;
        """,
            (CHARACTER_ID,),
        )

        room_description = cursor.fetchone()

        if not room_description:
            raise Exception("Room description not found.")

        # Get room exits
        cursor.execute(
            """
            SELECT rc.direction, r.name
            FROM RoomConnections rc
            JOIN Rooms r ON rc.to_room_id = r.id
            JOIN CharacterStates cs ON rc.from_room_id = cs.current_room_id
            JOIN Characters c ON cs.character_id = c.id
            WHERE c.discord_user_id = ?;
            """,
            (CHARACTER_ID,),
        )

        room_exits = cursor.fetchall()

        return room_description[0], room_exits if room_exits else None


def move_character(direction):
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Get current room
        cursor.execute(
            """
            SELECT r.id
            FROM Rooms r
            JOIN CharacterStates cs ON r.id = cs.current_room_id
            JOIN Characters c ON cs.character_id = c.id
            WHERE c.discord_user_id = ?;
            """,
            (CHARACTER_ID,),
        )

        current_room = cursor.fetchone()

        if not current_room:
            raise Exception("Current room not found.")

        # Get the exit for the given direction
        cursor.execute(
            """
            SELECT rc.to_room_id
            FROM RoomConnections rc
            WHERE rc.from_room_id = ? AND LOWER(rc.direction) = LOWER(?);
            """,
            (current_room[0], direction),
        )

        new_room = cursor.fetchone()

        if not new_room:
            raise Exception(f"No exit found in direction: {direction}")

        # Update character's current room
        cursor.execute(
            """
            UPDATE CharacterStates
            SET current_room_id = ?, updated_at = CURRENT_TIMESTAMP
            WHERE character_id = (SELECT id FROM Characters WHERE discord_user_id = ?);
            """,
            (new_room[0], CHARACTER_ID),
        )

        conn.commit()

        # Get characters new location
        cursor.execute(
            """
            SELECT Rooms.name, Rooms.description
            FROM Rooms
            JOIN CharacterStates ON Rooms.id = CharacterStates.current_room_id
            JOIN Characters ON CharacterStates.character_id = Characters.id
            WHERE Characters.discord_user_id = ?;
            """,
            (CHARACTER_ID,),
        )

        return cursor.fetchone()
