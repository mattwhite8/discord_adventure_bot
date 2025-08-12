import discord
from discord.ext import commands

from app.database.db_connector import initialize_db


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} ({bot.user.id})")

    try:
        initialize_db()
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise

    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(f"Error syncing commands: {e}")

@bot.tree.command(name="ping", description="Ping the bot to check if it's online.")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")
