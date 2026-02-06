import discord
import os
import asyncio
import aiohttp
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
intents.presences = True
intents.dm_messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    activities = [
        discord.Streaming(name="with My Pookie <3", url="https://www.twitch.tv/weebo64"),
        discord.Streaming(name="im silly :3", url="https://www.twitch.tv/weebo64"),
        discord.Streaming(name="type /help for commands", url="https://www.twitch.tv/weebo64"),
        discord.CustomActivity(name="Bot made by Weebo64!"),
    ]
    async def change_activity():
        while True:
            for activity in activities:
                try:
                    await bot.change_presence(activity=activity, status=discord.Status.dnd)
                except Exception as e:
                    print(f"⚠️ Failed to change presence: {e}")
                await asyncio.sleep(35)
    bot.loop.create_task(change_activity())
    await bot.tree.sync()
    print(f'✅ Bot is online! Logged in as {bot.user}')
    print(f'🌐 WeebOwO is in {len(bot.guilds)} servers:')
    await print_automod_status()

async def print_automod_status():
    token = os.getenv("DISCORD_TOKEN")
    headers = {
        "Authorization": f"Bot {token}",
        "Content-Type": "application/json"
    }
    async with aiohttp.ClientSession() as session:
        for guild in bot.guilds:
            url = f"https://discord.com/api/v10/guilds/{guild.id}/auto-moderation/rules"
            try:
                async with session.get(url, headers=headers) as resp:
                    rules = await resp.json()
                    found = False
                    if isinstance(rules, list):
                        for rule in rules:
                            if rule.get("name") == "Censored Language Filter":
                                found = True
                                break
                    status = "✅" if found else "❌"
                    print(f"{status} {guild.name} (ID: {guild.id})")
            except Exception as e:
                print(f"⚠️ {guild.name} (ID: {guild.id}): Error checking ({e})")

# Load all cogs
async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            ext = f'cogs.{filename[:-3]}'
            if ext not in bot.extensions:
                await bot.load_extension(ext)

async def main():
    await load_cogs()
    async with bot:
        await bot.start(TOKEN)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped manually.")
