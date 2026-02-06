import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import time
import sys
import subprocess

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.OWNER_ID = 257196097494188032

    @app_commands.command(name="help", description="Show all available commands for the bot")
    async def help(self, interaction: discord.Interaction):
        help_page1 = """**🎮 Fun Commands**  
`/weebowo` — Cute random images (Art by kytronix & funnyhoohooman)
`/cinema` — Sends the 'absolute_cinema.png' image
`/pat <user>` — Pat someone on the head
`/kiss <user>` — Give someone a kiss
`/slap <user>` — Slap someone
`/poke <user>` — Poke someone
`/bonk <user>` — Bonk someone (go to horny jail!)
`/ship <user1> <user2>` — Ship two users together with compatibility
`/8ball <question>` — Ask the magic 8-ball a question
`/car` — Get a funny, wholesome, cute, or silly cat gif
`/coinflip <heads/tails>` — Flip a coin and guess the result
`/dice [sides]` — Roll a dice (default 6 sides)
`/rps <choice>` — Rock, Paper, Scissors
`/choose <options>` — Let the bot choose from comma-separated options
`/rate <thing>` — Rate something from 0 to 10
`/say <message>` — The bot says your message
`/poll <question>` — Create a quick yes/no poll
`/hine` — Trust me bro

**✨ Text Fun Commands**
`/color <color> <text>` — Make your text appear in different colors
`/reverse <text>` — Reverse your text
`/mock <text>` — MoCk YoUr TeXt LiKe ThIs
`/uwuify <text>` — Make your text more uwu
`/ascii <text>` — Convert text to ASCII art (max 10 chars)
`/emojify <text>` — Convert text to emoji letters"""

        help_page2 = """**🎵 Music & Media Commands**  
`/vc` or `!vc` — Join your voice channel
`!play <url>` — Play audio from YouTube or Spotify
`/music <file>` — Upload and play your own file
`/download_mp3 <url>` — Download YouTube audio as MP3 (blocks copyrighted music)
`/embed_video <url>` — Download and send Instagram, TikTok, or Twitter/X videos
`/queue` — View the music queue
`/skip` — Skip to the next song
`/pause` — Pause music
`/resume` — Resume music
`/stop` — Stop playback and clear the queue
`!loop` — Loop the current song

**👮 Moderation & Admin**  
`/warn <user> <reason>` — Warn a user (Admin only)
`/remove_warnings <user>` — Clear all warnings from a user (Admin only)
`/purge <amount>` — Bulk delete messages (Admin only)
`/slowmode <seconds>` — Set slowmode for channel (Admin only)
`/lock [reason]` — Lock the current channel (Admin only)
`/unlock [reason]` — Unlock the current channel (Admin only)
`/say_in <channel_id> <message>` — Send message in specific channel (Admin only)
`/reply <user_id> <message>` — DM a message to someone
`!restart` — Restart the bot (Owner only)"""

        help_page3 = """**ℹ️ Utility & Info**  
`/help` — Show this help message
`/ping` — Check latency
`/afk [reason]` — Set yourself as AFK (auto-notifies when mentioned)
`/userinfo [user]` — Get info about a user
`/serverinfo` — Server details
`/servers` — List all servers bot is in (Owner only)
`/avatar [user]` — View user avatar (global & server)
`/show_warning` — Check your warning count
`/show_banned_words` — List all banned words
`/active_dev_badge` — Instructions for Active Developer Badge
`/terms` — Show the Terms of Service
`/website` — Get the link to Weebo's website
`/about` — Learn more about WeebOwO and her creators

**🎮 Mario Kart Wii**  
`/setfc <region> <modpack> <code>` — Add your friend code
`/fc [user]` — View friend codes

**⏰ Reminders**  
`/remindme <minutes> <message>` — Set a reminder (DMs you after delay)

**✨ Other**  
This bot also responds to DMs and TTS messages in the `#tts` channel when joined to a voice channel.

**Have fun with the bot :3**"""

        try:
            await interaction.user.send(help_page1)
            await interaction.user.send(help_page2)
            await interaction.user.send(help_page3)
            await interaction.response.send_message("📬 Check your DMs!", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("I couldn't send you a DM 😢 Make sure your DMs are open!", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Something went wrong: {e}", ephemeral=True)

    @app_commands.command(name="ping", description="Check the bot's latency.")
    async def ping(self, interaction: discord.Interaction):
        start_time = time.perf_counter()
        await interaction.response.send_message("🏓 Pinging...", ephemeral=True)
        end_time = time.perf_counter()
        latency = (end_time - start_time) * 1000
        websocket_latency = self.bot.latency * 1000
        await interaction.edit_original_response(content=f"🏓 Pong!\n🕒 Response Time: `{latency:.2f}ms`\n🌐 WebSocket Latency: `{websocket_latency:.2f}ms`")

    @app_commands.command(name="userinfo", description="Get information about a user.")
    @app_commands.describe(user="The user to get info about")
    async def userinfo(self, interaction: discord.Interaction, user: discord.Member = None):
        user = user or interaction.user
        embed = discord.Embed(title=f"User Info - {user}", color=discord.Color.blue())
        embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
        embed.add_field(name="ID", value=user.id)
        embed.add_field(name="Joined", value=user.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        embed.add_field(name="Account Created", value=user.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        embed.add_field(name="Roles", value=", ".join([role.name for role in user.roles if role.name != "@everyone"]) or "None", inline=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="serverinfo", description="Get information about this server.")
    async def serverinfo(self, interaction: discord.Interaction):
        guild = interaction.guild
        embed = discord.Embed(title=f"Server Info - {guild.name}", color=discord.Color.green())
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        embed.add_field(name="ID", value=guild.id)
        embed.add_field(name="Owner", value=guild.owner)
        embed.add_field(name="Members", value=guild.member_count)
        embed.add_field(name="Channels", value=len(guild.channels))
        embed.add_field(name="Created", value=guild.created_at.strftime("%Y-%m-%d %H:%M:%S"))
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="servers", description="List all servers the bot is in.")
    async def servers(self, interaction: discord.Interaction):
        if interaction.user.id != self.OWNER_ID:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        guilds = self.bot.guilds
        server_list = "\n".join(f"- {guild.name} (ID: {guild.id})" for guild in guilds)

        embed = discord.Embed(title=f"Servers I'm in ({len(guilds)})", description=server_list or "I'm not in any servers.", color=discord.Color.purple())
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="avatar", description="Get a user's avatar.")
    @app_commands.describe(user="The user to get the avatar of")
    async def avatar(self, interaction: discord.Interaction, user: discord.Member = None):
        user = user or interaction.user
        
        class AvatarView(discord.ui.View):
            def __init__(self, member: discord.Member):
                super().__init__(timeout=180)
                self.member = member
                
            @discord.ui.button(label="Global Avatar", style=discord.ButtonStyle.primary)
            async def global_avatar(self, interaction: discord.Interaction, button: discord.ui.Button):
                avatar_url = self.member.avatar.url if self.member.avatar else self.member.default_avatar.url
                embed = discord.Embed(title=f"{self.member}'s Global Avatar", color=discord.Color.purple())
                embed.set_image(url=avatar_url)
                await interaction.response.edit_message(embed=embed, view=self)
                
            @discord.ui.button(label="Server Avatar", style=discord.ButtonStyle.secondary)
            async def server_avatar(self, interaction: discord.Interaction, button: discord.ui.Button):
                if self.member.guild_avatar:
                    avatar_url = self.member.guild_avatar.url
                    embed = discord.Embed(title=f"{self.member}'s Server Avatar", color=discord.Color.purple())
                    embed.set_image(url=avatar_url)
                else:
                    avatar_url = self.member.avatar.url if self.member.avatar else self.member.default_avatar.url
                    embed = discord.Embed(title=f"{self.member}'s Avatar", description="No server-specific avatar set.", color=discord.Color.purple())
                    embed.set_image(url=avatar_url)
                await interaction.response.edit_message(embed=embed, view=self)
        
        avatar_url = user.avatar.url if user.avatar else user.default_avatar.url
        embed = discord.Embed(title=f"{user}'s Avatar", color=discord.Color.purple())
        embed.set_image(url=avatar_url)
        view = AvatarView(user)
        await interaction.response.send_message(embed=embed, view=view)

    @app_commands.command(name="poll", description="Create a quick poll (yes/no).")
    @app_commands.describe(question="The poll question")
    async def poll(self, interaction: discord.Interaction, question: str):
        embed = discord.Embed(title="📊 Poll", description=question, color=discord.Color.orange())
        msg = await interaction.channel.send(embed=embed)
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")
        await interaction.response.send_message("Poll created!", ephemeral=True)

    @app_commands.command(name="remindme", description="Set a reminder (DMs you after a delay).")
    @app_commands.describe(minutes="Minutes to wait", message="Reminder message")
    async def remindme(self, interaction: discord.Interaction, minutes: int, message: str):
        await interaction.response.send_message(f"⏰ I'll remind you in {minutes} minutes!", ephemeral=True)
        await asyncio.sleep(minutes * 60)
        try:
            await interaction.user.send(f"⏰ Reminder: {message}")
        except discord.Forbidden:
            pass

    @app_commands.command(name="reply", description="Send a message to a selected server member.")
    @app_commands.describe(user_id="The user ID of the member you want to reply to", message="The message to send to the member.")
    async def reply(self, interaction: discord.Interaction, user_id: str, message: str):
        await interaction.response.defer(ephemeral=True)
        await interaction.delete_original_response()
        try:
            user = await self.bot.fetch_user(user_id)
            await user.send(message)
            await interaction.followup.send(f"Message sent to {user.name}!", ephemeral=True)
        except discord.NotFound:
            await interaction.followup.send(f"User with ID {user_id} not found.", ephemeral=True)
        except discord.Forbidden:
            await interaction.followup.send(f"Couldn't send the message to {user.name}. They may have DMs disabled.", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"An error occurred: {str(e)}", ephemeral=True)

    @app_commands.command(name="say", description="The bot says something you write.")
    @app_commands.describe(message="The message to be said by the bot.")
    async def say(self, interaction: discord.Interaction, message: str):
        await interaction.response.send_message(message)

    @app_commands.command(name="say_in", description="The bot sends a message in a specific channel using its ID.")
    @app_commands.describe(channel_id="The ID of the channel to send the message in.", message="The message to send.")
    @app_commands.checks.has_permissions(administrator=True)
    async def say_in(self, interaction: discord.Interaction, channel_id: str, message: str):
        try:
            channel = interaction.guild.get_channel(int(channel_id))
            if not isinstance(channel, discord.TextChannel):
                await interaction.response.send_message("❌ Invalid channel ID or not a text channel.", ephemeral=True)
                return
        except Exception:
            await interaction.response.send_message("❌ Failed to find the channel. Check the channel ID.", ephemeral=True)
            return

        try:
            await channel.send(message)
            await interaction.response.send_message(f"✅ Message sent in {channel.mention}", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("❌ I don't have permission to send messages in that channel.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"⚠️ Error sending message: {e}", ephemeral=True)

    @say_in.error
    async def say_in_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            if not interaction.response.is_done():
                await interaction.response.send_message("❌ You don't have permission to use this command.", ephemeral=True)
        else:
            if not interaction.response.is_done():
                await interaction.response.send_message("⚠️ An unexpected error occurred.", ephemeral=True)
            raise error

    @app_commands.command(name="active_dev_badge", description="Helps you qualify for the Active Developer Badge.")
    async def active_dev_badge(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "✅ Slash command used! If you're the bot owner, you can now claim the badge at https://discord.com/developers/active-developer",
            ephemeral=True
        )

    @app_commands.command(name="terms", description="Show the Terms of Service for this bot.")
    async def terms(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "Terms of Service: https://pastebin.com/eCk6W69N Policy: https://pastebin.com/V8Vqdnkb",
            ephemeral=True
        )

    @app_commands.command(name="website", description="Get the link to Weebo's website.")
    async def weebo64_website(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "Weebo's Website: https://weebo64.is-a.dev/ :3c",
            ephemeral=False
        )

    @app_commands.command(name="about", description="Learn more about WeebOwO and her creators!")
    async def about(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="About WeebOwO",
            description="WeebOwO Discord bot is created by <@257196097494188032>!\n"
                        "She's a fun bot with lots of silly and useful commands:\n"
                        "• `/weebowo` — Cute random images\n"
                        "• `/play` — Play music\n"
                        "• `/poll` — Quick polls\n"
                        "• `/purge` — Bulk delete messages\n"
                        "• `/userinfo` — User info\n"
                        "• `/say` — Make the bot talk\n"
                        "She can also help moderate your server :3c\n\n"
                        "**Special thanks to these people for all the support:**\n"
                        "<@820190462253596702>\n"
                        "<@331794107791835136>\n"
                        "<@932671402543288321>\n"
                        "<@915664359194251266>\n"
                        "<@456569408135888938>\n\n"
                        "And you for using this bot! Thank you 💖\n\n"
                        "If you have any issues, please contact <@257196097494188032> on Discord :3c",
            color=discord.Color.purple()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @commands.command()
    async def restart(self, ctx):
        bot_owner_id = 257196097494188032

        if ctx.author.id != bot_owner_id and ctx.author.id != ctx.guild.owner_id:
            await ctx.send("You do not have permission to restart me >:<")
            return

        await ctx.send("nya~ :3c")

        python = sys.executable
        subprocess.Popen([python, "-m", "bot"])

        await self.bot.close()

async def setup(bot):
    await bot.add_cog(Utility(bot))
