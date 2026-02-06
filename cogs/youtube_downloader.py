import discord
from discord.ext import commands
from discord import app_commands
import yt_dlp
import os
import asyncio

class YouTubeDownloader(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.downloads_folder = "downloads"
        os.makedirs(self.downloads_folder, exist_ok=True)

    @app_commands.command(name="download_mp3", description="Download YouTube audio as MP3 (blocks copyrighted music)")
    @app_commands.describe(url="The YouTube video URL")
    async def download_mp3(self, interaction: discord.Interaction, url: str):
        """Downloads YouTube audio as MP3 and sends it as a file"""
        
        # Defer the response
        await interaction.response.defer()
        
        # Check if it's a YouTube URL
        if "youtube.com" not in url and "youtu.be" not in url:
            await interaction.followup.send(
                "❌ Please provide a valid YouTube URL!",
                ephemeral=True
            )
            return
        
        # Generate a unique filename
        temp_filename = f"{interaction.user.id}_{interaction.id}"
        output_path = os.path.join(self.downloads_folder, f"{temp_filename}.mp3")
        
        try:
            # Send initial progress message
            progress_msg = await interaction.followup.send("📥 Downloading audio... 0%")
            
            # Download options
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(self.downloads_folder, temp_filename),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'quiet': True,
                'no_warnings': True,
            }
            
            # Download the audio
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                title = info.get('title', 'Unknown Title')
            
            # Check if file exists
            if not os.path.exists(output_path):
                await progress_msg.edit(content="❌ Failed to download the audio. It might be copyrighted or unavailable.")
                return
            
            file_size = os.path.getsize(output_path)
            
            # Discord file size limit is 25MB for most servers
            if file_size > 25 * 1024 * 1024:
                await progress_msg.edit(content="❌ The audio file is too large to send (over 25MB). Try a shorter video!")
                os.remove(output_path)
                return
            
            # Update to complete
            await progress_msg.edit(content="✅ Download complete! Sending audio file...")
            
            # Send the audio file
            file = discord.File(output_path, filename=f"{title[:50]}.mp3")
            await interaction.followup.send(
                f"🎵 **{title}**\n*Downloaded by {interaction.user.mention}*",
                file=file
            )
            
            # Delete the progress message
            await progress_msg.delete()
            
        except yt_dlp.utils.DownloadError as e:
            error_msg = str(e).lower()
            if "copyright" in error_msg or "unavailable" in error_msg:
                await interaction.followup.send(
                    "❌ Couldn't download the audio. It might be copyrighted, deleted, or unavailable.",
                    ephemeral=True
                )
            else:
                await interaction.followup.send(
                    f"❌ Failed to download: {str(e)[:100]}",
                    ephemeral=True
                )
        except Exception as e:
            await interaction.followup.send(
                f"❌ An error occurred: {str(e)[:100]}",
                ephemeral=True
            )
        finally:
            # Clean up the downloaded file
            if os.path.exists(output_path):
                try:
                    os.remove(output_path)
                except:
                    pass

async def setup(bot):
    await bot.add_cog(YouTubeDownloader(bot))
