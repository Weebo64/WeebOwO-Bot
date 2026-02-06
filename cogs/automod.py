import discord
from discord import Interaction
from discord.ext import commands
from discord import app_commands
from datetime import timedelta
import aiohttp
import os
import json
import re

# Constants
LOG_CHANNEL_ID = 1386780509815705903
BANNED_WORDS_FILE = "cogs/banned_words.txt"
WARNINGS_FILE = "cogs/user_warnings.json"

FIRST_WARNING = 50
SECOND_WARNING = 100
THIRD_WARNING = 200

def load_banned_words(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return [line.strip().lower() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"⚠️ Warning: '{file_path}' not found. No banned words loaded.")
        return []
    except Exception as e:
        print(f"⚠️ Error loading banned words: {e}")
        return []

def load_warnings():
    if not os.path.exists(WARNINGS_FILE):
        return {}
    try:
        with open(WARNINGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ Error loading warnings: {e}")
        return {}

def save_warnings(warnings):
    try:
        with open(WARNINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(warnings, f, indent=4)
    except Exception as e:
        print(f"⚠️ Error saving warnings: {e}")

def contains_banned_word(text, banned_words):
    for word in banned_words:
        pattern = rf"\b{re.escape(word)}\b"
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False

class Automod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.censored_keywords = load_banned_words(BANNED_WORDS_FILE)
        self.user_warnings = load_warnings()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"✅ Automod ready. Loaded {len(self.censored_keywords)} banned words.")
        for guild in self.bot.guilds:
            await self.ensure_automod_rule(guild)
        try:
            await self.bot.tree.sync()
            print("✅ Slash commands synced globally.")
        except Exception as e:
            print(f"❌ Failed to sync slash commands globally: {e}")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await self.ensure_automod_rule(guild)
        try:
            await self.bot.tree.sync(guild=guild)
            print(f"✅ Slash commands synced for guild: {guild.name}")
        except Exception as e:
            print(f"❌ Failed to sync slash commands for guild {guild.name}: {e}")

    @commands.Cog.listener()
    async def on_guild_available(self, guild):
        await self.ensure_automod_rule(guild)

    async def ensure_automod_rule(self, guild):
        log_channel = discord.utils.get(guild.text_channels, name="logs")
        if not log_channel:
            log_channel = next((c for c in guild.text_channels if c.permissions_for(guild.me).send_messages), None)
        if not log_channel:
            print(f"No suitable log channel found in {guild.name}. Skipping AutoMod rule creation.")
            return

        payload = {
            "name": "Censored Language Filter",
            "event_type": 1,
            "trigger_type": 1,
            "trigger_metadata": {"keyword_filter": self.censored_keywords},
            "actions": [
                {"type": 1, "metadata": {}},
                {"type": 2, "metadata": {"channel_id": str(log_channel.id)}},
                {"type": 3, "metadata": {"duration_seconds": 600}}
            ],
            "enabled": True
        }

        token = os.getenv("DISCORD_TOKEN")
        if not token:
            print("❌ DISCORD_TOKEN not set in environment.")
            return

        url = f"https://discord.com/api/v10/guilds/{guild.id}/auto-moderation/rules"
        headers = {
            "Authorization": f"Bot {token}",
            "Content-Type": "application/json"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                rules = await resp.json()
                if isinstance(rules, list):
                    for rule in rules:
                        if rule["name"] == "Censored Language Filter":
                            return

            async with session.post(url, headers=headers, json=payload) as resp:
                if resp.status in (200, 201):
                    print(f"✅ AutoMod rule created for guild: {guild.name}")
                else:
                    print(f"❌ Failed to create AutoMod rule for {guild.name}: {resp.status}")
                    print(await resp.text())

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return

        if contains_banned_word(message.content, self.censored_keywords):
            try:
                await message.delete()
            except discord.Forbidden:
                pass

            user_id = str(message.author.id)
            guild_id = str(message.guild.id)

            if guild_id not in self.user_warnings:
                self.user_warnings[guild_id] = {}

            if user_id not in self.user_warnings[guild_id]:
                self.user_warnings[guild_id][user_id] = 1
            else:
                self.user_warnings[guild_id][user_id] += 1

            warning_count = self.user_warnings[guild_id][user_id]
            save_warnings(self.user_warnings)

            if warning_count == FIRST_WARNING:
                try:
                    await message.author.send(
                        f"⚠️ Warning {FIRST_WARNING}: You have been warned for using banned words in **{message.guild.name}**. Please be careful."
                    )
                except discord.Forbidden:
                    pass

            elif warning_count == SECOND_WARNING:
                try:
                    await message.author.timeout(timedelta(hours=1), reason=f"Automod: 2nd warning for inappropriate language.")
                    await message.author.send(
                        f"⏰ Warning {SECOND_WARNING}: This is your **2nd warning**. You have been timed out for **1 hour** in **{message.guild.name}** for repeated violations."
                    )
                except Exception as e:
                    print(f"❌ Failed to timeout user: {e}")

            elif warning_count >= THIRD_WARNING:
                try:
                    await message.author.send(
                        f"🚫 You have been **banned** from **{message.guild.name}** due to repeated violations. Please contact: @weebo64 for issues."
                    )
                except discord.Forbidden:
                    pass
                try:
                    await message.guild.ban(message.author, reason=f"Automod: {THIRD_WARNING} warnings for inappropriate language.")
                except discord.Forbidden:
                    log_channel = self.bot.get_channel(LOG_CHANNEL_ID)
                    if log_channel:
                        await log_channel.send(
                            f"❌ I do not have permission to ban {message.author.mention} in **{message.guild.name}**."
                        )
                self.user_warnings[guild_id].pop(user_id, None)
                save_warnings(self.user_warnings)

            # Logging the warning
            log_channel = self.bot.get_channel(LOG_CHANNEL_ID)
            if log_channel:
                embed = discord.Embed(
                    title="🚨 Automod Triggered",
                    description=(
                        f"**User:** {message.author.mention}\n"
                        f"**Guild:** {message.guild.name}\n"
                        f"**Channel:** {message.channel.mention}\n"
                        f"**Warnings:** {warning_count}/{THIRD_WARNING}"
                    ),
                    color=discord.Color.red()
                )
                embed.add_field(
                    name="Message Content",
                    value=discord.utils.escape_markdown(message.content)[:1024],
                    inline=False
                )
                embed.add_field(
                    name="Message Link",
                    value=f"[Jump to Message]({message.jump_url})",
                    inline=False
                )
                embed.set_footer(text=f"User ID: {message.author.id}")
                await log_channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Automod(bot))
