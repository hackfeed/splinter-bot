import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
bot = commands.Bot(command_prefix="!")


@bot.command(name="split")
@commands.has_role("Captain Flex")
async def split_users(ctx, users_per_team, base_channel, team_a_channel, team_b_channel, is_strict="нестрого"):
    guild = ctx.guild
    base = discord.utils.get(guild.voice_channels, name=base_channel)
    team_a = discord.utils.get(guild.voice_channels, name=team_a_channel)
    team_b = discord.utils.get(guild.voice_channels, name=team_b_channel)

    if not base:
        await ctx.send("❌ Не найден голосовой канал, из которого распределяются пользователи.")
        return
    if not team_a:
        await ctx.send("❌ Не найден голосовой канал, в который нужно распределить участников первой команды.")
        return
    if not team_b:
        await ctx.send("❌ Не найден голосовой канал, в который нужно распределить участников второй команды.")
        return

    users = base.members
    users_per_team = int(users_per_team)

    if len(users) < users_per_team:
        await ctx.send("❌ Невозможно распределить участников выбранным способом: количество пользователей меньше количества участников команды.")
        return

    if is_strict != "нестрого":
        if len(users) != users_per_team * 2:
            await ctx.send("❌ Невозможно поделить участников строго поровну. Деление не будет производиться.")
            return
        else:
            await ctx.send("🧱 Участники будут поделены строго поровну.")
    else:
        await ctx.send("🧲 Деление будет производиться по остаточному принципу. Возможно, одна из команд не досчитается игроков :(")

    team_a_membs = random.sample(users, users_per_team)
    team_b_membs = list(set(users) - set(team_a_membs))

    for user_a in team_a_membs:
        await user_a.move_to(team_a)

    for user_b in team_b_membs:
        await user_b.move_to(team_b)

bot.run(TOKEN)
