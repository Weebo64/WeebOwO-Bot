import discord
from discord.ext import commands
from discord import app_commands
import re

class Suggestions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="suggest", description="Submit a suggestion.")
    @app_commands.describe(text="Your suggestion")
    async def suggest(self, interaction: discord.Interaction, text: str):
        channel = discord.utils.get(interaction.guild.text_channels, name="suggestions")
        if channel:
            embed = discord.Embed(title="New Suggestion", color=discord.Color.blue())

            # Extract possible GIF or image URL
            url_match = re.search(r"(https?://\S+\.(?:gif|png|jpg|jpeg|webp))", text)
            if url_match:
                image_url = url_match.group(1)
                embed.set_image(url=image_url)
                # Remove image link from description
                text = text.replace(image_url, "").strip()

            embed.description = text if text else "No description provided."
            embed.set_footer(text=f"Suggested by {interaction.user}")
            msg = await channel.send(embed=embed)
            await msg.add_reaction("👍")
            await msg.add_reaction("👎")
            await interaction.response.send_message("Suggestion submitted!", ephemeral=True)
        else:
            await interaction.response.send_message("Suggestions channel not found.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Suggestions(bot))
