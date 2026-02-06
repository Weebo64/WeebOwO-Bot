import discord
from discord.ext import commands

class Goodbye(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = member.guild.get_channel(1381290120396804136)
        if channel:
            username = member.display_name
            # UwUfy the message
            uwu_message = f"oh nuuu, **{username}** weft the sewver :sob: see u watew and come back ;w;"
            await channel.send(uwu_message)

async def setup(bot):
    await bot.add_cog(Goodbye(bot))