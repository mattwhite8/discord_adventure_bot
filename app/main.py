from dotenv import load_dotenv

import os

from app.bot.bot import bot
import app.bot.commands

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")


if __name__ == "__main__":
    try:
        bot.run(DISCORD_TOKEN)
    except KeyboardInterrupt:
        print("Bot shutdown complete.")
