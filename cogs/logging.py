import discord
from discord.ext import commands

class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        channel = discord.utils.get(message.guild.text_channels, name="logs")
        if channel:
            await channel.send(f"🗑️ Message deleted in {message.channel.mention} by {message.author.mention}: {message.content}")

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        channel = discord.utils.get(guild.text_channels, name="logs")
        if channel:
            await channel.send(f"🔨 {user} was banned from the server.")

async def setup(bot):
    await bot.add_cog(Logging(bot))