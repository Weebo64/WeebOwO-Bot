import discord
from discord.ext import commands
from discord import app_commands
import random
import os
import aiohttp

class Images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.WEEBOWO_FOLDER = "WeebOwO"

    @app_commands.command(name="weebowo", description="Sends a random WeebOwO image with a cute message. (Art by kytronix & funnyhoohooman)")
    async def weebowo(self, interaction: discord.Interaction):
        """Sends a random image from the WeebOwO folder with a cute message"""
        await interaction.response.defer()

        if not os.path.exists(self.WEEBOWO_FOLDER):
            await interaction.followup.send("❌ The 'WeebOwO' folder doesn't exist!", ephemeral=True)
            return

        image_files = [f for f in os.listdir(self.WEEBOWO_FOLDER) if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        if not image_files:
            await interaction.followup.send("❌ No images found in the 'WeebOwO' folder.", ephemeral=True)
            return

        random_image = random.choice(image_files)
        image_path = os.path.join(self.WEEBOWO_FOLDER, random_image)

        cute_messages = [
            "Hope this makes your day better! 💖",
            "Stay cute and awesome! ✨",
            "Here's some OwO energy for you! 🥰",
            "UwU have a great day!",
            "Nyaa~ enjoy this! :3"
        ]
        message = random.choice(cute_messages)

        await interaction.followup.send(
            f"{interaction.user.mention} {message}",
            file=discord.File(image_path)
        )

    @app_commands.command(name="cinema", description="Sends the 'absolute_cinema.png' image.")
    async def cinema(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        await interaction.delete_original_response()
        cinema_image = discord.File("absolute_cimema.png")
        await interaction.channel.send(file=cinema_image)
        if getattr(interaction, "message", None) and interaction.message.reference:
            referenced_message = await interaction.channel.fetch_message(interaction.message.reference.message_id)
            if referenced_message.attachments:
                for attachment in referenced_message.attachments:
                    if attachment.url.endswith(('png', 'jpg', 'jpeg', 'gif')):
                        await referenced_message.delete()

    @app_commands.command(name="car", description="Get a funny, wholesome, cute, or silly cat gif!")
    async def car(self, interaction: discord.Interaction):
        search_terms = [
            "car cat",
            "silly cat",
            "freaky cat",
            "but here's the",
            "kitty review",
            "eepy car",
            "cat eepy",
            "cat review",
            "hachiware"
        ]

        async def get_cat_gif():
            async with aiohttp.ClientSession() as session:
                params = {
                    "q": random.choice(search_terms),
                    "key": os.getenv("TENOR_API_KEY"),
                    "limit": 25,
                    "media_filter": "minimal"
                }
                async with session.get("https://tenor.googleapis.com/v2/search", params=params) as resp:
                    if resp.status != 200:
                        print(f"❌ Tenor API error: {resp.status}")
                        return None
                    data = await resp.json()
                    results = data.get("results", [])
                    if results:
                        return random.choice(results)["media_formats"]["gif"]["url"]
            return None

        await interaction.response.defer()
        gif_url = await get_cat_gif()
        if gif_url:
            await interaction.followup.send(gif_url)
        else:
            await interaction.followup.send("😿 Couldn't find a cat gif right now.")

    @app_commands.command(name="hug", description="hug your favorite person!")
    @app_commands.describe(user="The user you want to hug")
    async def hug(self, interaction: discord.Interaction, user: discord.Member):
        async def get_tenor_gif(query):
            async with aiohttp.ClientSession() as session:
                params = {
                    "q": query,
                    "key": os.getenv("TENOR_API_KEY"),
                    "limit": 20,
                    "media_filter": "minimal"
                }
                async with session.get("https://tenor.googleapis.com/v2/search", params=params) as resp:
                    data = await resp.json()
                    results = data.get("results", [])
                    if results:
                        return random.choice(results)["media_formats"]["gif"]["url"]
            return None

        hug_messages = [
            "{sender} gives {receiver} a warm hug! 🤗",
            "{sender} wraps their arms around {receiver} tightly!",
            "{sender} sends a big fluffy hug to {receiver}!",
            "{sender} gives {receiver} the biggest hug ever!",
            "{sender} hugs {receiver} gently and smiles!",
            "{sender} gives {receiver} a surprise hug! 💜",
            "{sender} hugs {receiver} with all their heart!",
            "{sender} gives {receiver} a cozy hug!"
        ]

        # Self-hug
        if user.id == interaction.user.id:
            gif_url = await get_tenor_gif("anime hug")
            msg = f"aww...are you lonely, {user.mention}? ;w; I will hug you!"
            embed = discord.Embed(description=msg, color=discord.Color.pink())
            if gif_url:
                embed.set_image(url=gif_url)
            await interaction.response.send_message(embed=embed)
            return

        # Hugging the bot
        if user.id == interaction.client.user.id:
            gif_url = await get_tenor_gif("shy anime hug")
            msg = "O-oh, you want to hug me? S-sure~ *hugs you back* 💜"
            embed = discord.Embed(description=msg, color=discord.Color.pink())
            if gif_url:
                embed.set_image(url=gif_url)
            await interaction.response.send_message(embed=embed)
            return

        # Hugging another user
        gif_url = await get_tenor_gif("anime hug")
        message = random.choice(hug_messages).format(sender=interaction.user.mention, receiver=user.mention)
        embed = discord.Embed(description=message, color=discord.Color.pink())
        if gif_url:
            embed.set_image(url=gif_url)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Images(bot))
