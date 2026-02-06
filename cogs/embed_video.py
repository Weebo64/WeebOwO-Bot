import discord
from discord.ext import commands
from discord import app_commands
import yt_dlp
import os
import asyncio

class EmbedVideo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.downloads_folder = "video_downloads"
        os.makedirs(self.downloads_folder, exist_ok=True)
        self.current_progress = 0

    def progress_hook(self, d):
        """Hook to track download progress"""
        if d['status'] == 'downloading':
            if 'total_bytes' in d:
                percent = (d['downloaded_bytes'] / d['total_bytes']) * 100
            elif 'total_bytes_estimate' in d:
                percent = (d['downloaded_bytes'] / d['total_bytes_estimate']) * 100
            else:
                percent = 0
            self.current_progress = int(percent)
        elif d['status'] == 'finished':
            self.current_progress = 100

    @app_commands.command(name="embed_video", description="Download and send Instagram, TikTok, or Twitter/X videos")
    @app_commands.describe(url="The Instagram, TikTok, or Twitter/X video URL")
    async def embed_video(self, interaction: discord.Interaction, url: str):
        """Downloads and sends Instagram, TikTok, or Twitter/X videos as files"""
        
        # Defer the response
        await interaction.response.defer()
        
        platform = None
        
        # Check if it's an Instagram post/reel
        if "instagram.com" in url:
            platform = "Instagram"
        # Check if it's a TikTok video
        elif "tiktok.com" in url or "vm.tiktok.com" in url:
            platform = "TikTok"
        # Check if it's a Twitter/X video
        elif "twitter.com" in url or "x.com" in url or "t.co" in url:
            platform = "Twitter/X"
        else:
            await interaction.followup.send(
                "❌ Please provide a valid Instagram, TikTok, or Twitter/X video URL!",
                ephemeral=True
            )
            return
        
        # Generate a unique filename
        temp_filename = f"{interaction.user.id}_{interaction.id}"
        
        self.current_progress = 0
        progress_msg = None
        actual_file = None
        
        try:
            # Send initial progress message
            progress_msg = await interaction.followup.send(f"📥 Downloading {platform} video... 0%")
            
            # Download options
            ydl_opts = {
                'format': 'best[ext=mp4]/best',
                'outtmpl': os.path.join(self.downloads_folder, temp_filename + '.%(ext)s'),
                'quiet': True,
                'no_warnings': True,
                'progress_hooks': [self.progress_hook],
            }
            
            # Start download in background
            download_task = asyncio.create_task(
                asyncio.to_thread(self._download_video, ydl_opts, url)
            )
            
            # Update progress while downloading
            last_progress = 0
            while not download_task.done():
                await asyncio.sleep(0.5)
                if self.current_progress != last_progress:
                    last_progress = self.current_progress
                    await progress_msg.edit(content=f"📥 Downloading {platform} video... {self.current_progress}%")
            
            # Wait for download to complete
            await download_task
            
            # Find the downloaded file
            for ext in ['.mp4', '.webm', '.mkv', '.mov']:
                test_path = os.path.join(self.downloads_folder, f"{temp_filename}{ext}")
                if os.path.exists(test_path):
                    actual_file = test_path
                    break
            
            if not actual_file or not os.path.exists(actual_file):
                await progress_msg.edit(content="❌ Failed to download the video. It might be private or unavailable.")
                return
            
            file_size = os.path.getsize(actual_file)
            
            # Discord file size limit is 25MB for most servers
            if file_size > 25 * 1024 * 1024:
                await progress_msg.edit(content="❌ The video is too large to send (over 25MB). Try a shorter video!")
                os.remove(actual_file)
                return
            
            # Update to complete
            await progress_msg.edit(content=f"✅ Download complete! Sending {platform} video...")
            
            # Send the video file
            file = discord.File(actual_file, filename=f"{platform}_video.mp4")
            await interaction.followup.send(
                f"*Sent by {interaction.user.mention}*",
                file=file
            )
            
            # Delete the progress message
            await progress_msg.delete()
            
        except yt_dlp.utils.DownloadError as e:
            error_msg = str(e).lower()
            if "private" in error_msg or "unavailable" in error_msg or "login" in error_msg:
                if progress_msg:
                    await progress_msg.edit(content="❌ Couldn't download the video. It might be private, deleted, or require login.")
                else:
                    await interaction.followup.send(
                        "❌ Couldn't download the video. It might be private, deleted, or require login.",
                        ephemeral=True
                    )
            else:
                if progress_msg:
                    await progress_msg.edit(content=f"❌ Failed to download: {str(e)[:100]}")
                else:
                    await interaction.followup.send(
                        f"❌ Failed to download: {str(e)[:100]}",
                        ephemeral=True
                    )
        except Exception as e:
            if progress_msg:
                await progress_msg.edit(content=f"❌ An error occurred: {str(e)[:100]}")
            else:
                await interaction.followup.send(
                    f"❌ An error occurred: {str(e)[:100]}",
                    ephemeral=True
                )
        finally:
            # Clean up the downloaded file
            if actual_file and os.path.exists(actual_file):
                try:
                    os.remove(actual_file)
                except:
                    pass
    
    def _download_video(self, ydl_opts, url):
        """Helper method to download video in a thread"""
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

async def setup(bot):
    await bot.add_cog(EmbedVideo(bot))
