import discord

from app.bot.bot import bot
from app.services.database import (
    get_character_status,
    get_or_create_character,
    get_room_exits,
    move_character,
)


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


@bot.tree.command(name="look", description="Look around your current room")
async def look(interaction: discord.Interaction):
    try:
        room_name, room_exits = get_room_exits()

        embed = discord.Embed(
            title=f"🔍 You look around the {room_name}",
            description="You see the following exits:",
            color=discord.Color.blue(),
        )

        if room_exits:
            for exit in room_exits:
                embed.add_field(name=exit[0], value=f"{exit[1]}", inline=False)
        else:
            embed.add_field(
                name="No Exits", value="You can't see any exits.", inline=False
            )

        await interaction.response.send_message(embed=embed)
    except Exception as e:
        print(f"Error looking around: {e}")
        await interaction.response.send_message(
            "❌ Failed to look around. Try `/begin_adventure` first!", ephemeral=True
        )


@bot.tree.command(name="go", description="Go to a different room")
async def go(interaction: discord.Interaction, direction: str):
    # Normalize direction, n -> north, s -> south, etc.
    direction_mapping = {
        "n": "north",
        "s": "south",
        "e": "east",
        "w": "west",
    }
    normalized_direction = direction_mapping.get(direction.lower(), direction)

    # if direction is not valid, return an error message
    if normalized_direction not in direction_mapping.values():
        await interaction.response.send_message(
            "❌ Invalid direction. Please use north, south, east, or west.",
            ephemeral=True,
        )
        return

    try:
        new_location = move_character(normalized_direction)

        embed = discord.Embed(
            title=f"🚶‍♂️ Moving {normalized_direction}",
            description=f"You move {normalized_direction} and arrive at:\n\n"
            f"**{new_location[0]}**\n{new_location[1]}",
            color=discord.Color.green(),
        )

        await interaction.response.send_message(embed=embed)
    except Exception as e:
        print(f"Error moving character: {e}")
        await interaction.response.send_message(
            "❌ Failed to move. Try `/begin_adventure` first!", ephemeral=True
        )
