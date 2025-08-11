## Discord Adventure Bot

A Discord bot for a text-based adventure game. Users explore rooms, interact with the world, and manage their character state—all via Discord commands.

### Features

- Connects to Discord using [discord.py](https://discordpy.readthedocs.io/)
- Persistent game world and player state stored in SQLite
- Database migrations for schema and initial world setup
- Room navigation and connections
- Character creation and management
- Extensible for new commands and features

### Database Structure

- **Rooms**: Defines locations in the game world
- **RoomConnections**: Maps navigable directions between rooms
- **Characters**: Associates Discord users with in-game characters
- **CharacterStates**: Tracks each character's current location

Migrations are managed automatically on startup from `app/database/migrations/`.

### Setup

1. **Clone the repository**

2. **Install dependencies**

   ```
   pip install -r requirements.txt
   ```

3. **Configure environment variables**

   - Copy `.env.example` to `.env`
   - Set your Discord bot token in `.env`

4. **Run the bot**
   ```
   python app/main.py
   ```

On first run, the database will be initialized and migrations applied.

### Development

- All database code is in `app/database/`
- Migrations are SQL files in `app/database/migrations/`
- Bot logic and commands are in `app/`

### Requirements

- Python 3.8+
- discord.py==2.5.2
- python-dotenv==1.1.1

### License

MIT License
