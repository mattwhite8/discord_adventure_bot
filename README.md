## Discord Adventure Bot

A Discord bot for a text-based adventure game built with Python and SQLite. Players can explore rooms, navigate between locations, and manage their character state through Discord slash commands.

### Features

- **Discord Integration**: Built with [discord.py](https://discordpy.readthedocs.io/) using slash commands
- **Persistent Game World**: SQLite database stores rooms, connections, and player states
- **Automatic Database Migrations**: Schema and world data managed through SQL migration files
- **Room-based Navigation**: Move between connected rooms using directional commands
- **Character Management**: Automatic character creation and state tracking per Discord user
- **Adventure Reset**: Players can restart their adventure at any time

### Available Commands

- `/begin_adventure` - Start or restart your adventure from the beginning
- `/status` - Check your current location and room description
- `/look` - See available exits from your current room
- `/go <direction>` - Move in a direction (north, south, east, west, or n/s/e/w)

### Project Structure

```
app/
├── bot/
│   ├── bot.py           # Discord bot setup and event handlers
│   └── commands.py      # Slash command implementations
├── database/
│   ├── db_connector.py  # Database connection and migration management
│   └── migrations/
│       ├── 001_initial_schema.sql     # Core database tables
│       └── 002_initial_world_state.sql # Sample rooms and connections
└── services/
    └── database.py      # Game logic and database operations
```

### Database Schema

The game uses SQLite with the following core tables:

- **Rooms**: Game locations with names and descriptions
- **RoomConnections**: Directional links between rooms (north, south, east, west)
- **Characters**: Maps Discord users to in-game characters
- **CharacterStates**: Tracks each character's current room location
- **Migrations**: Manages database schema versioning

### Setup Instructions

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd discord_adventure_bot
   ```

2. **Create a virtual environment** (recommended)

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Discord Bot**

   - Create a new application at [Discord Developer Portal](https://discord.com/developers/applications)
   - Create a bot user and copy the token
   - Enable necessary bot permissions and slash commands

5. **Configure environment**

   ```bash
   cp .env.example .env
   # Edit .env and add your Discord bot token
   ```

6. **Run the bot**
   ```bash
   python app/main.py
   ```

The database will be automatically initialized on first run, applying all migrations and creating the sample world.

### Development

- **Adding new rooms**: Create SQL migration files in `app/database/migrations/`
- **New commands**: Add slash commands in `app/bot/commands.py`
- **Game logic**: Extend database operations in `app/services/database.py`
- **Database changes**: Use numbered migration files (e.g., `003_new_feature.sql`)

### Sample World

The initial world includes:

- **Entrance Hall**: Starting location with marble floors and pillars
- **Library**: Quiet room with ancient books (north of entrance)
- **Armory**: Weapon storage room (east of entrance)

### Requirements

- Python 3.8+
- discord.py==2.5.2
- python-dotenv==1.1.1

### License

MIT License
