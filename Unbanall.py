# Made by .aydenn. and gabriel

# -----------------
# imoorts
# -----------------
import discord
from discord.ext import commands
import aiohttp
import asyncio
from concurrent.futures import ThreadPoolExecutor
import os

# -----------------
# title
# -----------------
os.system(f'cls & mode 85,20 & title unbanall')

# -----------------
# Config
# -----------------
bot_prefix = 'un!' # bot prefix
bot_token = '' # bot token

# -----------------
# Source code
# -----------------
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=bot_prefix, intents=intents) 
thread_pool = ThreadPoolExecutor()

@bot.event
async def on_ready():
    print('Made by aydenn and gabriel.')
    print(f'Logged in as {bot.user.name}')

async def unban_user(session, guild_id, token, user_id):
    headers = {
        'Authorization': f'Bot {token}'
    }
    async with session.delete(f'https://discord.com/api/v10/guilds/{guild_id}/bans/{user_id}', headers=headers) as response:
        if response.status == 204:
            print(f"Unbanned user {user_id}")
        else:
            print(f"Failed to unban user {user_id} - Status: {response.status}")

@bot.command()
async def unbanall(ctx: commands.Context):
    bans = [ban_entry.user.id async for ban_entry in ctx.guild.bans()]

    async with aiohttp.ClientSession() as session:
        tasks = [unban_user(session, ctx.guild.id, bot.http.token, user_id) for user_id in bans]
        await asyncio.gather(*tasks)

    await ctx.send("Unbanned all users")

bot.run(bot_token) # running the bot
