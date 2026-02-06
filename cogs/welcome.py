import discord
from discord.ext import commands
import random

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        
        # Check if the bot is mentioned and the message contains "reference sheets"
        if self.bot.user in message.mentions and "reference sheets" in message.content.lower():
            await message.channel.send(
                "ohhh :0 you wanna draw meeeee?? that's so sweet!! >w<\n"
                "hehe of course you can!! weebo already posted my reference sheets on his twitter~ :3\n"
                "here ya go -> https://x.com/weebo64/status/1829576079973237128\n"
                "can't wait to see what you make!! :3c"
            )

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        """Detects when a member boosts the server and sends a wholesome message"""
        if not before.premium_since and after.premium_since:
            announcement_channel_id = 1392214225597759498
            channel = self.bot.get_channel(announcement_channel_id)
            
            if channel:
                boost_messages = [
                    f"oh yippiieee {after.mention} boosted Weebo's server! omgomg omg tyyy <333",
                    f"aaaaa {after.mention} just boosted the server!! you're so sweet tysm!! 💖✨",
                    f"omg omg {after.mention} boosted!! Weebo is so happy rn!! thank you so much!! 🥺💕"
                ]
                
                message = random.choice(boost_messages)
                await channel.send(message)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        """Sends a DM to the person who added the bot when it joins a new server"""
        try:
            # Try to find the person who added the bot by checking audit logs
            async for entry in guild.audit_logs(limit=10, action=discord.AuditLogAction.bot_add):
                if entry.target.id == self.bot.user.id:
                    inviter = entry.user
                    
                    # Send a friendly DM to the person who added the bot
                    try:
                        await inviter.send(
                            f"heyyy thank you so much for trusting me, WeebOwO, to your server **{guild.name}**! "
                            f"we're going to have so much fun together :3c\n\n"
                            f"if you got any questions feel free to dm <@257196097494188032> on discord or "
                            f"join his server at discord.gg/3knu2FNqDG in the \"#help-about-the-bot\" channel, "
                            f"maybe he can help you there!\n\n"
                            f"use `/help` to see all my commands and get started~ 💖"
                        )
                        print(f"✅ Sent welcome DM to {inviter} ({inviter.id}) for adding bot to {guild.name}")
                    except discord.Forbidden:
                        print(f"❌ Could not DM {inviter} - they have DMs disabled")
                    except Exception as e:
                        print(f"❌ Error sending DM to {inviter}: {e}")
                    break
        except discord.Forbidden:
            print(f"❌ Missing permissions to check audit logs in {guild.name}")
        except Exception as e:
            print(f"❌ Error in on_guild_join for {guild.name}: {e}")

async def setup(bot):
    await bot.add_cog(Welcome(bot))
