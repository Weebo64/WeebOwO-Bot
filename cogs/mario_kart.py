import discord
from discord.ext import commands
from discord import app_commands
import json
import os
import re

class MarioKart(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.fc_file = os.path.join("cogs", "user_fcs.json")

    @app_commands.command(name="setfc", description="Add your friend code for a specific region and modpack.")
    @app_commands.describe(
        region="Select your region",
        modpack="Select the modpack",
        friend_code="Your friend code in format: xxxx-xxxx-xxxx"
    )
    @app_commands.choices(region=[
        app_commands.Choice(name="PAL", value="PAL"),
        app_commands.Choice(name="NTSC-U", value="NTSC-U"),
        app_commands.Choice(name="NTSC-J", value="NTSC-J"),
        app_commands.Choice(name="NTSC-K", value="NTSC-K")
    ], modpack=[
        app_commands.Choice(name="Retro Rewind", value="Retro Rewind"),
        app_commands.Choice(name="Insane Kart Wii", value="Insane Kart Wii"),
        app_commands.Choice(name="Other", value="Other")
    ])
    async def setfc(self, interaction: discord.Interaction, region: app_commands.Choice[str], modpack: app_commands.Choice[str], friend_code: str):
        await interaction.response.defer(ephemeral=True)
        
        # Validate friend code format
        if not re.match(r'^\d{4}-\d{4}-\d{4}$', friend_code):
            await interaction.followup.send("❌ Invalid friend code format! Please use: `xxxx-xxxx-xxxx` (e.g., `1234-5678-9012`)")
            return
        
        # Load existing FC data
        if os.path.exists(self.fc_file):
            with open(self.fc_file, "r", encoding="utf-8") as f:
                fc_data = json.load(f)
        else:
            fc_data = {}
        
        user_id = str(interaction.user.id)
        if user_id not in fc_data:
            fc_data[user_id] = {"username": interaction.user.name, "fcs": []}
        
        # Check if this exact FC already exists
        fc_exists = False
        for fc_entry in fc_data[user_id]["fcs"]:
            if (fc_entry["region"] == region.value and 
                fc_entry["modpack"] == modpack.value and 
                fc_entry["code"] == friend_code):
                fc_exists = True
                break
        
        if fc_exists:
            await interaction.followup.send(
                f"⚠️ You already have this friend code registered!\n"
                f"**Region:** {region.value}\n"
                f"**Modpack:** {modpack.value}\n"
                f"**FC:** `{friend_code}`"
            )
            return
        
        # Add the new FC
        fc_entry = {
            "region": region.value,
            "modpack": modpack.value,
            "code": friend_code
        }
        
        fc_data[user_id]["fcs"].append(fc_entry)
        action = "added"
        
        # Update username in case it changed
        fc_data[user_id]["username"] = interaction.user.name
        
        # Save to file
        with open(self.fc_file, "w", encoding="utf-8") as f:
            json.dump(fc_data, f, indent=4)
        
        await interaction.followup.send(
            f"✅ Successfully {action} your friend code!\n"
            f"**Region:** {region.value}\n"
            f"**Modpack:** {modpack.value}\n"
            f"**FC:** `{friend_code}`"
        )

    @app_commands.command(name="fc", description="View your or another user's friend codes.")
    @app_commands.describe(user="The user whose friend codes you want to see (optional)")
    async def fc(self, interaction: discord.Interaction, user: discord.Member = None):
        target_user = user or interaction.user
        
        # Load FC data
        if not os.path.exists(self.fc_file):
            await interaction.response.send_message("❌ No friend codes have been registered yet!", ephemeral=True)
            return
        
        with open(self.fc_file, "r", encoding="utf-8") as f:
            fc_data = json.load(f)
        
        user_id = str(target_user.id)
        if user_id not in fc_data or not fc_data[user_id]["fcs"]:
            await interaction.response.send_message(
                f"❌ {target_user.mention} hasn't registered any friend codes yet!\n"
                f"Use `/setfc` to add your friend codes.",
                ephemeral=True
            )
            return
        
        # Organize FCs by region
        regions = {}
        for fc_entry in fc_data[user_id]["fcs"]:
            region = fc_entry["region"]
            if region not in regions:
                regions[region] = []
            regions[region].append(f"`{fc_entry['code']}` ({fc_entry['modpack']})")
        
        # Build description
        description = ""
        for region in ["PAL", "NTSC-U", "NTSC-J", "NTSC-K"]:
            if region in regions:
                description += f"**{region}:**\n"
                for fc_line in regions[region]:
                    description += f"• {fc_line}\n"
                description += "\n"
        
        embed = discord.Embed(
            title=f"🎮 {target_user.name}'s Friend Codes",
            description=description.strip(),
            color=discord.Color.green()
        )
        embed.set_thumbnail(url=target_user.avatar.url if target_user.avatar else target_user.default_avatar.url)
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(MarioKart(bot))
