import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")


bot = commands.Bot(command_prefix="!")


@bot.event
async def on_ready():
    my_guild = None
    for guild in bot.guilds:
        if guild.name == "MSHP Test Server":
            my_guild = guild

    for channel in my_guild.channels:
        print(channel)


@bot.command(name="split")
async def split_users(ctx, users_per_team, base_channel, team_a_channel, team_b_channel):
    guild = ctx.guild
    base = discord.utils.get(guild.voice_channels, name=base_channel)
    team_a = discord.utils.get(guild.voice_channels, name=team_a_channel)
    team_b = discord.utils.get(guild.voice_channels, name=team_b_channel)

    users = base.members

    team_a_membs = random.sample(users, int(users_per_team))
    team_b_membs = list(set(users) - set(team_a_membs))

    for user_a in team_a_membs:
        await user_a.move_to(team_a)

    for user_b in team_b_membs:
        await user_b.move_to(team_b)

bot.run(TOKEN)
