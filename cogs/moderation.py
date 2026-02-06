import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import json
import os

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.warnings_path = os.path.join("cogs", "user_warnings.json")
        self.banned_words_path = os.path.join("cogs", "banned_words.txt")

    @app_commands.command(name="ban", description="Ban a user from the server.")
    @app_commands.describe(user="User to ban", reason="Reason for ban")
    async def ban(self, interaction: discord.Interaction, user: discord.Member, reason: str = "No reason provided"):
        # Permission check
        if not interaction.user.guild_permissions.ban_members:
            await interaction.response.send_message("You don't have permission to ban members.", ephemeral=True)
            return

        # Try to DM the user first
        try:
            await user.send(
                f"You have been banned from **{interaction.guild.name}** by **{interaction.user}**.\nReason: {reason}"
            )
        except discord.Forbidden:
            pass  # User has DMs closed or blocked the bot

        # Ban the user
        try:
            await user.ban(reason=f"{reason} (Banned by {interaction.user})")
        except discord.Forbidden:
            await interaction.response.send_message("I don't have permission to ban that user.", ephemeral=True)
            return
        except discord.HTTPException:
            await interaction.response.send_message("Banning failed due to an error.", ephemeral=True)
            return

        # Confirm ban in channel
        await interaction.response.send_message(f"{user} has been banned. Reason: {reason}")

        # Optionally delete the confirmation after 30 seconds
        await asyncio.sleep(30)
        try:
            msg = await interaction.original_response()
            await msg.delete()
        except Exception:
            pass

    @app_commands.command(name="kick", description="Kick a user from the server.")
    @app_commands.describe(user="User to kick", reason="Reason for kick")
    async def kick(self, interaction: discord.Interaction, user: discord.Member, reason: str = "No reason provided"):
        # Permission check for the user running the command
        if not interaction.user.guild_permissions.kick_members:
            await interaction.response.send_message("❌ You don't have permission to kick members.", ephemeral=True)
            return
        
        # Check if trying to kick themselves
        if user.id == interaction.user.id:
            await interaction.response.send_message("❌ You can't kick yourself!", ephemeral=True)
            return
        
        # Check if trying to kick the bot
        if user.id == interaction.client.user.id:
            await interaction.response.send_message("❌ I can't kick myself!", ephemeral=True)
            return
        
        # Check if trying to kick the server owner
        if user.id == interaction.guild.owner_id:
            await interaction.response.send_message("❌ You can't kick the server owner!", ephemeral=True)
            return
        
        # Check role hierarchy - bot's top role must be higher than target's top role
        if interaction.guild.me.top_role <= user.top_role:
            await interaction.response.send_message("❌ I can't kick this user because their role is higher than or equal to mine!", ephemeral=True)
            return
        
        # Check if the command user's role is high enough
        if interaction.user.top_role <= user.top_role and interaction.user.id != interaction.guild.owner_id:
            await interaction.response.send_message("❌ You can't kick this user because their role is higher than or equal to yours!", ephemeral=True)
            return

        # Try to DM the user first
        try:
            await user.send(
                f"You have been kicked from **{interaction.guild.name}** by **{interaction.user}**.\nReason: {reason}"
            )
        except discord.Forbidden:
            pass  # User has DMs closed or blocked the bot

        # Kick the user
        try:
            await user.kick(reason=f"{reason} (Kicked by {interaction.user})")
        except discord.Forbidden:
            await interaction.response.send_message("❌ I don't have permission to kick that user. Make sure I have the 'Kick Members' permission!", ephemeral=True)
            return
        except discord.HTTPException as e:
            await interaction.response.send_message(f"❌ Kicking failed: {e}", ephemeral=True)
            return

        # Confirm kick in channel
        await interaction.response.send_message(f"✅ {user} has been kicked. Reason: {reason}")

        # Optionally delete the confirmation after 30 seconds
        await asyncio.sleep(30)
        try:
            msg = await interaction.original_response()
            await msg.delete()
        except Exception:
            pass

    @app_commands.command(name="warn", description="Warn a user for breaking rules. (Admin only)")
    @app_commands.describe(user="The user to warn", reason="Reason for the warning")
    @app_commands.checks.has_permissions(administrator=True)
    async def warn(self, interaction: discord.Interaction, user: discord.Member, reason: str = "No reason provided"):
        # Load or create warnings file
        if os.path.exists(self.warnings_path):
            try:
                with open(self.warnings_path, "r", encoding="utf-8") as f:
                    warnings = json.load(f)
            except Exception:
                warnings = {}
        else:
            warnings = {}
        
        guild_id = str(interaction.guild.id)
        user_id = str(user.id)
        
        # Initialize guild and user if needed
        if guild_id not in warnings:
            warnings[guild_id] = {}
        if user_id not in warnings[guild_id]:
            warnings[guild_id][user_id] = 0
        
        # Add warning
        warnings[guild_id][user_id] += 1
        warning_count = warnings[guild_id][user_id]
        
        # Save warnings
        with open(self.warnings_path, "w", encoding="utf-8") as f:
            json.dump(warnings, f, indent=4)
        
        # Send response
        await interaction.response.send_message(
            f"⚠️ {user.mention} has been warned.\n**Reason:** {reason}\n**Total Warnings:** {warning_count}",
            ephemeral=False
        )
        
        # Try to DM the user
        try:
            await user.send(f"your silly ass got a warning for **{reason}**, that means you got {warning_count} warnings >:3c")
        except discord.Forbidden:
            pass

    @warn.error
    async def warn_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            if not interaction.response.is_done():
                await interaction.response.send_message("❌ You don't have permission to use this command.", ephemeral=True)

    @app_commands.command(name="remove_warnings", description="Remove all warnings from a user. (Admin only)")
    @app_commands.describe(user="The user whose warnings will be removed.")
    async def remove_warnings(self, interaction: discord.Interaction, user: discord.Member):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ You must be an administrator to use this command.", ephemeral=True)
            return

        # Load warnings
        if not os.path.exists(self.warnings_path):
            await interaction.response.send_message("ℹ️ Warning file not found.", ephemeral=True)
            return

        try:
            with open(self.warnings_path, "r", encoding="utf-8") as f:
                warnings = json.load(f)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error reading warnings file: {e}", ephemeral=True)
            return

        guild_id = str(interaction.guild.id)
        user_id = str(user.id)

        removed_any = False

        # Remove warnings if exist
        if guild_id in warnings and user_id in warnings[guild_id]:
            del warnings[guild_id][user_id]
            if not warnings[guild_id]:
                del warnings[guild_id]
            removed_any = True

            with open(self.warnings_path, "w", encoding="utf-8") as f:
                json.dump(warnings, f, indent=4)

        if removed_any:
            await interaction.response.send_message(f"✅ Cleared all warnings for {user.mention}. The next violation will start at 1 warning.", ephemeral=True)
        else:
            await interaction.response.send_message(f"ℹ️ {user.mention} has no warnings in this server.", ephemeral=True)

    @app_commands.command(name="show_warning", description="Check how many warnings you have.")
    async def show_warning(self, interaction: discord.Interaction):
        if not os.path.exists(self.warnings_path):
            await interaction.response.send_message("⚠️ No warning data file found.", ephemeral=True)
            return

        try:
            with open(self.warnings_path, "r", encoding="utf-8") as f:
                warnings = json.load(f)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error reading warnings: `{e}`", ephemeral=True)
            return

        guild_id = str(interaction.guild.id)
        user_id = str(interaction.user.id)

        count = warnings.get(guild_id, {}).get(user_id, 0)

        await interaction.response.send_message(
            f"⚠️ You have **{count}** warning(s) in this server.", ephemeral=True
        )

    @app_commands.command(name="show_banned_words", description="List all banned words.")
    async def show_banned_words(self, interaction: discord.Interaction):
        if not os.path.exists(self.banned_words_path):
            await interaction.response.send_message("🚫 No banned words file found.", ephemeral=True)
            return

        with open(self.banned_words_path, "r", encoding="utf-8") as f:
            banned_words = [line.strip() for line in f if line.strip()]

        if not banned_words:
            await interaction.response.send_message("✅ There are no banned words configured.", ephemeral=True)
            return

        chunks = [", ".join(banned_words[i:i+50]) for i in range(0, len(banned_words), 50)]
        embed = discord.Embed(title="🚫 Banned Words", description=chunks[0], color=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="purge", description="Bulk delete messages (admin only).")
    @app_commands.describe(amount="Number of messages to delete (max 100)")
    async def purge(self, interaction: discord.Interaction, amount: int):
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
            return
        deleted = await interaction.channel.purge(limit=min(amount, 100))
        await interaction.response.send_message(f"Deleted {len(deleted)} messages.", ephemeral=True)

    @app_commands.command(name="slowmode", description="Set slowmode for the current channel. (Admin only)")
    @app_commands.describe(seconds="Slowmode delay in seconds (0 to disable, max 21600)")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def slowmode(self, interaction: discord.Interaction, seconds: int):
        if seconds < 0 or seconds > 21600:
            await interaction.response.send_message("❌ Slowmode must be between 0 and 21600 seconds (6 hours).", ephemeral=True)
            return
        
        try:
            await interaction.channel.edit(slowmode_delay=seconds)
            if seconds == 0:
                await interaction.response.send_message("✅ Slowmode has been disabled.", ephemeral=False)
            else:
                await interaction.response.send_message(f"✅ Slowmode set to {seconds} seconds.", ephemeral=False)
        except discord.Forbidden:
            await interaction.response.send_message("❌ I don't have permission to edit this channel.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

    @slowmode.error
    async def slowmode_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            if not interaction.response.is_done():
                await interaction.response.send_message("❌ You don't have permission to use this command.", ephemeral=True)

    @app_commands.command(name="lock", description="Lock the current channel. (Admin only)")
    @app_commands.describe(reason="Reason for locking the channel")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def lock(self, interaction: discord.Interaction, reason: str = "No reason provided"):
        try:
            overwrite = interaction.channel.overwrites_for(interaction.guild.default_role)
            overwrite.send_messages = False
            await interaction.channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
            await interaction.response.send_message(f"🔒 Channel locked.\n**Reason:** {reason}", ephemeral=False)
        except discord.Forbidden:
            await interaction.response.send_message("❌ I don't have permission to lock this channel.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

    @lock.error
    async def lock_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            if not interaction.response.is_done():
                await interaction.response.send_message("❌ You don't have permission to use this command.", ephemeral=True)

    @app_commands.command(name="unlock", description="Unlock the current channel. (Admin only)")
    @app_commands.describe(reason="Reason for unlocking the channel")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def unlock(self, interaction: discord.Interaction, reason: str = "No reason provided"):
        try:
            overwrite = interaction.channel.overwrites_for(interaction.guild.default_role)
            overwrite.send_messages = True
            await interaction.channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
            await interaction.response.send_message(f"🔓 Channel unlocked.\n**Reason:** {reason}", ephemeral=False)
        except discord.Forbidden:
            await interaction.response.send_message("❌ I don't have permission to unlock this channel.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

    @unlock.error
    async def unlock_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            if not interaction.response.is_done():
                await interaction.response.send_message("❌ You don't have permission to use this command.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Moderation(bot))
