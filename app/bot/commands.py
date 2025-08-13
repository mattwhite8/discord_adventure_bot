import discord

from app.bot.bot import bot
from app.services.database import get_character_status, get_or_create_character


@bot.tree.command(name="begin_adventure", description="Start a new adventure")
async def begin_adventure(interaction: discord.Interaction):
    try:
        character_name = get_or_create_character()

        embed = discord.Embed(
            title="⚔️ Adventure Begins!",
            description=f"**{character_name}** enters the dungeon once more...\n\n"
            f"The adventure has been reset to the beginning.\n"
            f"Use `/status` to see where you are!",
            color=discord.Color.green(),
        )

        await interaction.response.send_message(embed=embed)
    except Exception as e:
        print(f"Error starting adventure: {e}")
        await interaction.response.send_message(
            "❌ Failed to start adventure. Check the logs.", ephemeral=True
        )


@bot.tree.command(name="status", description="Check your character status")
async def status(interaction: discord.Interaction):
    try:
        room_name, description = get_character_status()

        embed = discord.Embed(
            title=f"📍 Current Location: {room_name}",
            description=description,
            color=discord.Color.blue(),
        )

        await interaction.response.send_message(embed=embed)
    except Exception as e:
        print(f"Error getting character status: {e}")
        await interaction.response.send_message(
            "❌ Failed to get status. Try `/begin_adventure` first!", ephemeral=True
        )
