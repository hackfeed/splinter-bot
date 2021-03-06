import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv

import meta


load_dotenv()
TOKEN = os.getenv("TOKEN")
bot = commands.Bot(command_prefix="!")


@bot.command(name="split")
@commands.has_role("Captain Flex")
async def split_users(ctx, users_per_team, base_channel, team_a_channel, team_b_channel, is_strict=meta.NOT_STRICT):
    guild = ctx.guild
    base = discord.utils.get(guild.voice_channels, name=base_channel)
    team_a = discord.utils.get(guild.voice_channels, name=team_a_channel)
    team_b = discord.utils.get(guild.voice_channels, name=team_b_channel)

    if not base:
        await ctx.send(meta.NO_BASE_CHANNEL_MSG)
        return
    if not team_a:
        await ctx.send(meta.NO_TEAM_A_CHANNEL_MSG)
        return
    if not team_b:
        await ctx.send(meta.NO_TEAM_B_CHANNEL_MSG)
        return

    users = base.members
    users_per_team = int(users_per_team)

    if len(users) < users_per_team:
        await ctx.send(meta.TEAM_GT_USERS_MSG)
        return

    if is_strict != meta.NOT_STRICT:
        if len(users) != users_per_team * 2:
            await ctx.send(meta.CANT_DIVIDE_STRICT_MSG)
            return
        else:
            await ctx.send(meta.STRICT_DIVISION_MSG)
    else:
        await ctx.send(meta.NONSTRICT_DIVISION_MSG)

    team_a_membs = random.sample(users, users_per_team)
    team_b_membs = list(set(users) - set(team_a_membs))

    for user_a in team_a_membs:
        await user_a.move_to(team_a)

    for user_b in team_b_membs:
        await user_b.move_to(team_b)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MissingRole):
        await ctx.send(meta.MISSING_ROLE_MSG)

if __name__ == "__main__":
    bot.run(TOKEN)
