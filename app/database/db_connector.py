import sqlite3
from contextlib import contextmanager
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MIGRATIONS_PATH = BASE_DIR / "migrations"
DB_PATH = BASE_DIR / "database.db"


@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    try:
        yield conn
    except sqlite3.Error as e:
        print(f"Database error occurred: {e}")
    finally:
        conn.close()


def initialize_db():
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Create Migrations table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Migrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                migration_name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()

        # Select all migration_names from Migrations table
        cursor.execute("SELECT migration_name FROM Migrations")
        applied_migrations = {migration[0] for migration in cursor.fetchall()}

        # Pending migrations
        migration_files = sorted(MIGRATIONS_PATH.glob("*.sql"))

        for migration_file in migration_files:
            if migration_file.name not in applied_migrations:
                print(f"Applying migration: {migration_file.name}")

                # Each migration is its own transaction
                try:
                    with open(migration_file, "r") as file:
                        sql_script = file.read()

                    cursor.executescript(sql_script)

                    cursor.execute(
                        """
                        INSERT INTO Migrations (migration_name) VALUES (?);
                    """,
                        (migration_file.name,),
                    )

                    conn.commit()
                    print(f"✓ Completed: {migration_file.name}")
                except sqlite3.Error as e:
                    print(f"✗ Failed: {migration_file.name}: {e}")
                    conn.rollback()
                    raise

        cursor.close()
