import discord
from discord.ext import commands
from discord import app_commands
import json
import os
from datetime import datetime

class AFKSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.afk_file = "cogs/afk_users.json"
        self.afk_users = self.load_afk_users()

    def load_afk_users(self):
        """Load AFK users from JSON file"""
        if os.path.exists(self.afk_file):
            try:
                with open(self.afk_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def save_afk_users(self):
        """Save AFK users to JSON file"""
        with open(self.afk_file, 'w', encoding='utf-8') as f:
            json.dump(self.afk_users, f, indent=4)

    @app_commands.command(name="afk", description="Set yourself as AFK with an optional reason")
    @app_commands.describe(reason="Why you're going AFK (optional)")
    async def afk(self, interaction: discord.Interaction, reason: str = None):
        """Set user as AFK"""
        
        guild_id = str(interaction.guild.id)
        user_id = str(interaction.user.id)
        
        if guild_id not in self.afk_users:
            self.afk_users[guild_id] = {}
        
        afk_reason = reason if reason else "AFK"
        timestamp = datetime.now().isoformat()
        
        self.afk_users[guild_id][user_id] = {
            "reason": afk_reason,
            "timestamp": timestamp
        }
        
        self.save_afk_users()
        
        embed = discord.Embed(
            description=f"💤 {interaction.user.mention} is now AFK: **{afk_reason}**",
            color=discord.Color.blue()
        )
        
        await interaction.response.send_message(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        """Check for AFK users in messages"""
        
        # Ignore bot messages
        if message.author.bot:
            return
        
        guild_id = str(message.guild.id)
        user_id = str(message.author.id)
        
        # Check if the message author is AFK and remove them
        if guild_id in self.afk_users and user_id in self.afk_users[guild_id]:
            afk_data = self.afk_users[guild_id][user_id]
            del self.afk_users[guild_id][user_id]
            
            if not self.afk_users[guild_id]:
                del self.afk_users[guild_id]
            
            self.save_afk_users()
            
            embed = discord.Embed(
                description=f"💚 Welcome back {message.author.mention}! I removed your AFK status~",
                color=discord.Color.green()
            )
            
            await message.channel.send(embed=embed, delete_after=5)
        
        # Check if any mentioned users are AFK
        if message.mentions:
            for mentioned_user in message.mentions:
                mentioned_id = str(mentioned_user.id)
                
                if guild_id in self.afk_users and mentioned_id in self.afk_users[guild_id]:
                    afk_data = self.afk_users[guild_id][mentioned_id]
                    reason = afk_data["reason"]
                    
                    # Calculate time since AFK
                    try:
                        afk_time = datetime.fromisoformat(afk_data["timestamp"])
                        time_diff = datetime.now() - afk_time
                        
                        if time_diff.days > 0:
                            time_str = f"{time_diff.days} day(s) ago"
                        elif time_diff.seconds >= 3600:
                            hours = time_diff.seconds // 3600
                            time_str = f"{hours} hour(s) ago"
                        elif time_diff.seconds >= 60:
                            minutes = time_diff.seconds // 60
                            time_str = f"{minutes} minute(s) ago"
                        else:
                            time_str = "just now"
                    except:
                        time_str = "a while ago"
                    
                    embed = discord.Embed(
                        description=f"💤 {mentioned_user.mention} is currently AFK: **{reason}**\n*Set {time_str}*",
                        color=discord.Color.blue()
                    )
                    
                    await message.channel.send(embed=embed, delete_after=10)
                    break  # Only show one AFK notification per message

async def setup(bot):
    await bot.add_cog(AFKSystem(bot))
