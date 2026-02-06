import discord
from discord.ext import commands
from discord import app_commands
import yt_dlp
import os
import asyncio
from collections import deque
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_client = None
        self.song_queue = deque()
        self.music_queue = []
        self.text_channel = None
        self.loop_song = False
        self.UPLOADS_FOLDER = "uploads"
        os.makedirs(self.UPLOADS_FOLDER, exist_ok=True)
        
        # Spotify credentials
        self.spotify = Spotify(client_credentials_manager=SpotifyClientCredentials(
            client_id='07511d9c93eb455fbe6f33659c9c9374',
            client_secret='a669fa41793e491baf495fc7b4cbe5c2'))

    @app_commands.command(name="vc", description="Make the bot join your current voice channel.")
    async def vc_slash(self, interaction: discord.Interaction):
        if not interaction.user.voice or not interaction.user.voice.channel:
            await interaction.response.send_message("❌ You must be in a voice channel for me to join!", ephemeral=True)
            return

        channel = interaction.user.voice.channel
        if interaction.guild.voice_client:
            self.voice_client = interaction.guild.voice_client
            await interaction.response.send_message(f"I'm already in {self.voice_client.channel.mention}!", ephemeral=True)
            return

        try:
            self.voice_client = await channel.connect()
            await interaction.response.send_message(f"✅ Joined {channel.mention}!", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Failed to join: {e}", ephemeral=True)

    @commands.command(name="vc")
    async def vc_prefix(self, ctx):
        if not ctx.author.voice or not ctx.author.voice.channel:
            await ctx.send("❌ You must be in a voice channel for me to join!", delete_after=5)
            await ctx.message.delete()
            return

        channel = ctx.author.voice.channel
        if ctx.guild.voice_client:
            self.voice_client = ctx.guild.voice_client
            await ctx.send(f"I'm already in {self.voice_client.channel.mention}!", delete_after=5)
            await ctx.message.delete()
            return

        try:
            self.voice_client = await channel.connect()
            await ctx.send(f"✅ Joined {channel.mention}!", delete_after=5)
        except Exception as e:
            await ctx.send(f"❌ Failed to join: {e}", delete_after=5)
        await ctx.message.delete()

    @commands.command()
    async def play(self, ctx, url: str = None):
        """Joins the voice channel and plays high-quality audio instantly from a YouTube or Spotify link"""
        if not ctx.author.voice:
            await ctx.send("You need to join a voice channel first.")
            return

        self.text_channel = ctx.channel

        if not self.voice_client or not self.voice_client.is_connected():
            channel = ctx.author.voice.channel
            self.voice_client = await channel.connect()

        if not url:
            if self.music_queue:
                await self.play_next_song_music_from_ctx(ctx)
                return
            else:
                await ctx.send("No uploaded music in the queue. Please upload a file with /music or provide a URL.")
                return

        if "youtube.com" in url or "youtu.be" in url:
            ydl_opts = {
                'format': 'bestaudio/best',
                'quiet': True,
                'noplaylist': True,
                'default_search': 'ytsearch',
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                try:
                    info = ydl.extract_info(url, download=False)
                    audio_url = info['url']
                    title = info.get('title', 'Unknown Title')
                    source = 'YouTube'
                except Exception as e:
                    await ctx.send(f"Failed to extract audio: {e}")
                    return
        elif "spotify.com" in url:
            track_id = url.split("/")[-1].split("?")[0]
            try:
                track = self.spotify.track(track_id)
                title = track['name']
                audio_url = track['preview_url']
                source = 'Spotify'
                if not audio_url:
                    await ctx.send("Spotify track preview is not available.")
                    return
            except Exception as e:
                await ctx.send(f"Failed to fetch Spotify track: {e}")
                return
        else:
            await ctx.send("Unsupported URL. Please provide a YouTube or Spotify link.")
            return

        self.song_queue.append((audio_url, title, source))
        if len(self.song_queue) == 1:
            await self.play_next_song()

    async def play_next_song(self):
        if not self.song_queue:
            await self.text_channel.send("🔇 The queue is empty.")
            return
        audio_url, title, source = self.song_queue.popleft()
        def after_play(e):
            fut = asyncio.run_coroutine_threadsafe(self.play_next_song(), self.bot.loop)
            try:
                fut.result()
            except Exception:
                pass
        self.voice_client.play(discord.FFmpegPCMAudio(audio_url), after=after_play)
        await self.text_channel.send(f"🎶 Now playing: **{title}** ({source})")

    async def play_next_song_music_from_ctx(self, ctx):
        if not self.music_queue:
            await ctx.send("🔇 The queue is empty.")
            await self.voice_client.disconnect()
            return
        _, file_path, user = self.music_queue[0]
        self.voice_client.play(discord.FFmpegPCMAudio(file_path), after=lambda e: asyncio.run_coroutine_threadsafe(self.play_finished_ctx(ctx), self.bot.loop))
        await ctx.send(f"🎶 Now playing: {os.path.basename(file_path)} (Added by {user.display_name})")

    async def play_finished_ctx(self, ctx):
        if self.music_queue:
            _, file_path, _ = self.music_queue.pop(0)
            os.remove(file_path)
            await self.play_next_song_music_from_ctx(ctx)
        else:
            await ctx.send("🔚 No more songs in the queue. Disconnecting.")
            await self.voice_client.disconnect()

    @commands.command()
    async def loop(self, ctx):
        """Loops the current song."""
        if not self.voice_client or not self.voice_client.is_connected():
            await ctx.send("I'm not in a voice channel!")
            return
        if self.voice_client.is_playing():
            self.loop_song = not self.loop_song
            if self.loop_song:
                await ctx.send("🔁 Looping the current song!")
            else:
                await ctx.send("🔁 Looping disabled!")
        else:
            await ctx.send("There is no song playing right now.")

    @app_commands.command(name="music", description="Upload a music file for the bot to play (only if it's in voice chat).")
    async def music(self, interaction: discord.Interaction, file: discord.Attachment):
        if not self.voice_client or not self.voice_client.is_connected():
            await interaction.response.send_message("❌ I must be in a voice channel to play music!", ephemeral=True)
            return
        if not file.filename.endswith((".mp3", ".wav", ".ogg")):
            await interaction.response.send_message("❌ Please upload a valid audio file (.mp3, .wav, .ogg).", ephemeral=True)
            return
        file_path = os.path.join(self.UPLOADS_FOLDER, file.filename)
        await file.save(file_path)
        self.music_queue.append((interaction, file_path, interaction.user))
        await interaction.response.send_message(f"🎵 Added to queue: **{file.filename}** by {interaction.user.display_name}")

        if not self.voice_client.is_playing():
            await self.play_next_song_music(interaction)

    async def play_next_song_music(self, interaction):
        if not self.music_queue:
            await interaction.followup.send("🔇 The queue is empty.")
            return
        _, file_path, user = self.music_queue[0]
        self.voice_client.play(discord.FFmpegPCMAudio(file_path), after=lambda e: asyncio.run_coroutine_threadsafe(self.play_finished(interaction), self.bot.loop))
        await interaction.followup.send(f"🎶 Now playing: {os.path.basename(file_path)} (Added by {user.display_name})")

    async def play_finished(self, interaction):
        if self.music_queue:
            _, file_path, _ = self.music_queue.pop(0)
            os.remove(file_path)
            await self.play_next_song_music(interaction)

    @app_commands.command(name="queue", description="View the current music queue.")
    async def queue(self, interaction: discord.Interaction):
        if not self.music_queue:
            await interaction.response.send_message("🔇 The queue is empty.", ephemeral=True)
            return
        queue_info = "\n".join([f"{i+1}. {os.path.basename(file_path)} (Added by {user.display_name})"
                               for i, (_, file_path, user) in enumerate(self.music_queue)])
        await interaction.response.send_message(f"🎵 Current Queue:\n{queue_info}", ephemeral=True)

    @app_commands.command(name="skip", description="Skip to the next song in the queue.")
    async def skip(self, interaction: discord.Interaction):
        if not self.music_queue:
            await interaction.response.send_message("🔇 The queue is empty.", ephemeral=True)
            return
        self.voice_client.stop()
        await self.play_next_song_music(interaction)
        await interaction.response.send_message("⏭️ Skipping to the next song.")

    @app_commands.command(name="pause", description="Pause the current song.")
    async def pause(self, interaction: discord.Interaction):
        if not self.voice_client or not self.voice_client.is_connected():
            await interaction.response.send_message("I'm not in a voice channel!", ephemeral=True)
            return
        if self.voice_client.is_playing():
            self.voice_client.pause()
            await interaction.response.send_message("⏸️ Paused the audio!", ephemeral=True)
        else:
            await interaction.response.send_message("There is no audio playing right now.", ephemeral=True)

    @app_commands.command(name="resume", description="Resume the paused song.")
    async def resume(self, interaction: discord.Interaction):
        if not self.voice_client or not self.voice_client.is_connected():
            await interaction.response.send_message("I'm not in a voice channel!", ephemeral=True)
            return
        if self.voice_client.is_paused():
            self.voice_client.resume()
            await interaction.response.send_message("▶️ Resumed the audio!", ephemeral=True)
        else:
            await interaction.response.send_message("There is no audio paused right now.", ephemeral=True)

    @app_commands.command(name="stop", description="Stop playback and clear the queue.")
    async def stop(self, interaction: discord.Interaction):
        if self.voice_client and self.voice_client.is_playing():
            self.voice_client.stop()
        self.music_queue.clear()
        await interaction.response.send_message("🛑 Stopped playback and cleared the queue.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Music(bot))
