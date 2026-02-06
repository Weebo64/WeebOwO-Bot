import discord
from discord.ext import commands

class ActionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Example: {message_id: {emoji: role_id}}
        self.role_messages = {}

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # Example: Give a role when a user reacts to a specific message
        # You need to set up self.role_messages with your message/emoji/role mapping
        if payload.message_id in self.role_messages:
            guild = self.bot.get_guild(payload.guild_id)
            role_id = self.role_messages[payload.message_id].get(str(payload.emoji))
            if role_id:
                role = guild.get_role(role_id)
                member = guild.get_member(payload.user_id)
                if role and member:
                    await member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.message_id in self.role_messages:
            guild = self.bot.get_guild(payload.guild_id)
            role_id = self.role_messages[payload.message_id].get(str(payload.emoji))
            if role_id:
                role = guild.get_role(role_id)
                member = guild.get_member(payload.user_id)
                if role and member:
                    await member.remove_roles(role)

async def setup(bot):
    await bot.add_cog(ActionRoles(bot))