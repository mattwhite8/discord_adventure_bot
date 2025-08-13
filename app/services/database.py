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
