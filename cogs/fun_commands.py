import discord
from discord.ext import commands
from discord import app_commands
import random

class FunCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ship", description="Ship two users together and see their compatibility!")
    @app_commands.describe(user1="First person to ship", user2="Second person to ship")
    async def ship(self, interaction: discord.Interaction, user1: discord.Member, user2: discord.Member):
        """Ships two users together with a compatibility percentage"""
        
        # Generate a consistent percentage based on user IDs
        combined_id = user1.id + user2.id
        random.seed(combined_id)
        compatibility = random.randint(0, 100)
        random.seed()  # Reset seed
        
        # Create ship name
        name1 = user1.display_name
        name2 = user2.display_name
        ship_name = name1[:len(name1)//2] + name2[len(name2)//2:]
        
        # Determine message based on compatibility
        if compatibility >= 90:
            message = "omg they're perfect together!! 💕💕"
            heart = "💖"
        elif compatibility >= 70:
            message = "aww they'd be so cute together~ 💗"
            heart = "💕"
        elif compatibility >= 50:
            message = "hmm maybe they could work out? 💭"
            heart = "💝"
        elif compatibility >= 30:
            message = "ehh not really feeling it... 😅"
            heart = "💔"
        else:
            message = "oof... maybe not the best match >w<"
            heart = "💔"
        
        # Create progress bar
        filled = int(compatibility / 10)
        bar = "█" * filled + "░" * (10 - filled)
        
        embed = discord.Embed(
            title=f"💘 Shipping {user1.display_name} x {user2.display_name}",
            description=f"**Ship Name:** {ship_name}\n\n{bar} **{compatibility}%**\n\n{message}",
            color=discord.Color.pink()
        )
        embed.set_footer(text=f"Requested by {interaction.user.display_name}")
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="pat", description="Pat someone on the head!")
    @app_commands.describe(user="The person to pat")
    async def pat(self, interaction: discord.Interaction, user: discord.Member):
        """Pat someone on the head with a cute message and anime GIF"""
        import aiohttp
        import os
        
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
        
        # Easter egg: User pats themselves
        if user.id == interaction.user.id:
            gif_url = await get_tenor_gif("anime pat head")
            msg = f"hey silly, you cannot pat yourself x3 here lemme do it for chu {user.mention}!! *pat pat* 💕"
            embed = discord.Embed(description=msg, color=discord.Color.from_rgb(255, 182, 193))
            if gif_url:
                embed.set_image(url=gif_url)
            await interaction.response.send_message(embed=embed)
            return
        
        # Easter egg: User pats the bot
        if user.id == interaction.client.user.id:
            gif_url = await get_tenor_gif("anime pat head")
            msg = "yippieee more pats for meeeeee :3 💕✨"
            embed = discord.Embed(description=msg, color=discord.Color.from_rgb(255, 182, 193))
            if gif_url:
                embed.set_image(url=gif_url)
            await interaction.response.send_message(embed=embed)
            return
        
        # Easter egg: User pats hinepare
        if user.id == 1216427362581876837:
            gif_url = await get_tenor_gif("anime pat head")
            msg = f"huh? why would chu pat a bot? she goes beep beep boop 🤖 hehe just kidding i will pat her for chu {interaction.user.mention}!! *pats {user.mention}* 💕"
            embed = discord.Embed(description=msg, color=discord.Color.from_rgb(255, 182, 193))
            if gif_url:
                embed.set_image(url=gif_url)
            await interaction.response.send_message(embed=embed)
            return
        
        # Normal pat messages
        pat_messages = [
            f"*pats {user.mention} on the head* 💕",
            f"{user.mention} *gets headpats!!* uwu",
            f"*pat pat* {user.mention} you're doing great!! >w<",
            f"{user.mention} *receives gentle headpats* 🥰",
            f"*gives {user.mention} lots of headpats!!* :3",
        ]
        
        # Get a random pat GIF from Tenor
        gif_url = await get_tenor_gif("anime pat head")
        message = random.choice(pat_messages)
        
        embed = discord.Embed(
            description=message,
            color=discord.Color.from_rgb(255, 182, 193)
        )
        embed.set_author(
            name=f"{interaction.user.display_name} pats {user.display_name}!",
            icon_url=interaction.user.display_avatar.url
        )
        
        if gif_url:
            embed.set_image(url=gif_url)
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="8ball", description="Ask the magic 8-ball a question!")
    @app_commands.describe(question="Your yes/no question")
    async def eightball(self, interaction: discord.Interaction, question: str):
        """Magic 8-ball with cute WeebOwO responses"""
        
        responses = [
            # Positive
            ("yes yes!! definitely!! >w<", discord.Color.green()),
            ("omg yes!! absolutely!! 💕", discord.Color.green()),
            ("mhm mhm!! i think so!! :3", discord.Color.green()),
            ("yep yep!! for sure!! ✨", discord.Color.green()),
            ("without a doubt!! uwu", discord.Color.green()),
            
            # Neutral
            ("hmm... maybe? 🤔", discord.Color.gold()),
            ("ask me again later!! >w<", discord.Color.gold()),
            ("i'm not sure about that one... 💭", discord.Color.gold()),
            ("ehh it's hard to say... 😅", discord.Color.gold()),
            ("the future is unclear!! ✨", discord.Color.gold()),
            
            # Negative
            ("nope nope!! don't think so >w<", discord.Color.red()),
            ("mm... probably not... 😔", discord.Color.red()),
            ("i don't think that's gonna happen... :c", discord.Color.red()),
            ("definitely not!! sorry!! 💔", discord.Color.red()),
            ("nah i wouldn't count on it...", discord.Color.red()),
        ]
        
        response, color = random.choice(responses)
        
        embed = discord.Embed(
            title="🎱 Magic 8-Ball",
            description=f"**Question:** {question}\n\n**Answer:** {response}",
            color=color
        )
        embed.set_footer(text=f"Asked by {interaction.user.display_name}")
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="color", description="Make your text appear in different colors!")
    @app_commands.describe(
        color="Choose a color for your text",
        text="The text you want to colorize"
    )
    @app_commands.choices(color=[
        app_commands.Choice(name="🔴 Red", value="red"),
        app_commands.Choice(name="🟢 Green", value="green"),
        app_commands.Choice(name="🟡 Yellow", value="yellow"),
        app_commands.Choice(name="🔵 Blue", value="blue"),
        app_commands.Choice(name="🟣 Purple", value="purple"),
        app_commands.Choice(name="🟠 Orange", value="orange"),
        app_commands.Choice(name="⚪ White", value="white"),
        app_commands.Choice(name="⚫ Gray", value="gray"),
    ])
    async def color(self, interaction: discord.Interaction, color: str, text: str):
        """Display text in different colors using ANSI codes"""
        
        # ANSI color codes for Discord
        color_codes = {
            "red": "\u001b[0;31m",
            "green": "\u001b[0;32m",
            "yellow": "\u001b[0;33m",
            "blue": "\u001b[0;34m",
            "purple": "\u001b[0;35m",
            "orange": "\u001b[0;31m",  # Orange uses red with different styling
            "white": "\u001b[0;37m",
            "gray": "\u001b[0;30m",
        }
        
        # Special handling for orange (uses bold red)
        if color == "orange":
            colored_text = f"\u001b[1;31m{text}\u001b[0m"
        else:
            colored_text = f"{color_codes[color]}{text}\u001b[0m"
        
        # Send the colored text in an ANSI code block
        await interaction.response.send_message(f"```ansi\n{colored_text}\n```")

    @app_commands.command(name="hine", description="trust me bro")
    async def hine(self, interaction: discord.Interaction):
        """Pings Hine with the hine.jpg image - with button choice"""
        
        class HineView(discord.ui.View):
            def __init__(self, bot):
                super().__init__(timeout=60)
                self.bot = bot
                
            @discord.ui.button(label="✅ sure", style=discord.ButtonStyle.success)
            async def yes_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                hine_user = await self.bot.fetch_user(1216427362581876837)
                await interaction.response.send_message(
                    f"{hine_user.mention}",
                    file=discord.File("hine.jpg")
                )
                
            @discord.ui.button(label="❌ nah bruh", style=discord.ButtonStyle.danger)
            async def no_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                await interaction.response.send_message(
                    "hine:",
                    file=discord.File("hine.jpg")
                )
        
        view = HineView(self.bot)
        await interaction.response.send_message(
            "do you want to ping hine? yes or nah",
            view=view,
            ephemeral=True
        )

    @app_commands.command(name="kiss", description="Give someone a kiss!")
    @app_commands.describe(user="The person to kiss")
    async def kiss(self, interaction: discord.Interaction, user: discord.Member):
        """Kiss someone with a cute message and anime GIF"""
        import aiohttp
        import os
        
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
        
        if user.id == interaction.user.id:
            gif_url = await get_tenor_gif("anime kiss")
            msg = f"silly {user.mention}!! chu can't kiss yourself!! >w<"
            embed = discord.Embed(description=msg, color=discord.Color.from_rgb(255, 105, 180))
            if gif_url:
                embed.set_image(url=gif_url)
            await interaction.response.send_message(embed=embed)
            return
        
        kiss_messages = [
            f"*kisses {user.mention}* 💋✨",
            f"{user.mention} *gets a kiss!!* >///< 💕",
            f"*smooch!!* {user.mention} 😘",
            f"{user.mention} *receives a gentle kiss* 💖",
            f"*gives {user.mention} a kiss!!* uwu 💋",
        ]
        
        gif_url = await get_tenor_gif("anime kiss")
        message = random.choice(kiss_messages)
        
        embed = discord.Embed(description=message, color=discord.Color.from_rgb(255, 105, 180))
        embed.set_author(
            name=f"{interaction.user.display_name} kisses {user.display_name}!",
            icon_url=interaction.user.display_avatar.url
        )
        
        if gif_url:
            embed.set_image(url=gif_url)
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="slap", description="Slap someone!")
    @app_commands.describe(user="The person to slap")
    async def slap(self, interaction: discord.Interaction, user: discord.Member):
        """Slap someone with a cute message and anime GIF"""
        import aiohttp
        import os
        
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
        
        if user.id == interaction.user.id:
            gif_url = await get_tenor_gif("anime slap")
            msg = f"ouchie!! {user.mention} why would chu slap yourself?? >w<"
            embed = discord.Embed(description=msg, color=discord.Color.orange())
            if gif_url:
                embed.set_image(url=gif_url)
            await interaction.response.send_message(embed=embed)
            return
        
        slap_messages = [
            f"*slaps {user.mention}* 👋",
            f"{user.mention} *gets slapped!!* oof!!",
            f"*SLAP!!* {user.mention} what did chu do?? >:c",
            f"{user.mention} *receives a slap* ouch!!",
            f"*slaps {user.mention} across the face!!* 😤",
        ]
        
        gif_url = await get_tenor_gif("anime slap")
        message = random.choice(slap_messages)
        
        embed = discord.Embed(description=message, color=discord.Color.orange())
        embed.set_author(
            name=f"{interaction.user.display_name} slaps {user.display_name}!",
            icon_url=interaction.user.display_avatar.url
        )
        
        if gif_url:
            embed.set_image(url=gif_url)
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="poke", description="Poke someone!")
    @app_commands.describe(user="The person to poke")
    async def poke(self, interaction: discord.Interaction, user: discord.Member):
        """Poke someone with a cute message and anime GIF"""
        import aiohttp
        import os
        
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
        
        poke_messages = [
            f"*pokes {user.mention}* 👉",
            f"{user.mention} *gets poked!!* hey!! >w<",
            f"*poke poke* {user.mention} hehe :3",
            f"{user.mention} *receives a poke* uwu",
            f"*pokes {user.mention} repeatedly!!* 👉👉👉",
        ]
        
        gif_url = await get_tenor_gif("anime poke")
        message = random.choice(poke_messages)
        
        embed = discord.Embed(description=message, color=discord.Color.blue())
        embed.set_author(
            name=f"{interaction.user.display_name} pokes {user.display_name}!",
            icon_url=interaction.user.display_avatar.url
        )
        
        if gif_url:
            embed.set_image(url=gif_url)
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="bonk", description="Bonk someone!")
    @app_commands.describe(user="The person to bonk")
    async def bonk(self, interaction: discord.Interaction, user: discord.Member):
        """Bonk someone with a cute message and anime GIF"""
        import aiohttp
        import os
        
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
        
        bonk_messages = [
            f"*bonks {user.mention}* 🔨 go to horny jail!!",
            f"{user.mention} *gets bonked!!* BONK!! 🔨",
            f"*BONK!!* {user.mention} no horny!! >:c",
            f"{user.mention} *receives a bonk* ouch!! 🔨",
            f"*bonks {user.mention} on the head!!* bad!! 🔨",
        ]
        
        gif_url = await get_tenor_gif("anime bonk")
        message = random.choice(bonk_messages)
        
        embed = discord.Embed(description=message, color=discord.Color.red())
        embed.set_author(
            name=f"{interaction.user.display_name} bonks {user.display_name}!",
            icon_url=interaction.user.display_avatar.url
        )
        
        if gif_url:
            embed.set_image(url=gif_url)
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="coinflip", description="Flip a coin and guess heads or tails!")
    @app_commands.describe(choice="Choose heads or tails")
    @app_commands.choices(choice=[
        app_commands.Choice(name="Heads", value="heads"),
        app_commands.Choice(name="Tails", value="tails")
    ])
    async def coinflip(self, interaction: discord.Interaction, choice: app_commands.Choice[str]):
        """Flip a coin and see if you guessed correctly"""
        result = random.choice(["heads", "tails"])
        user_choice = choice.value
        won = user_choice == result
        
        emoji = "🪙" if result == "heads" else "🎴"
        result_display = "Heads" if result == "heads" else "Tails"
        choice_display = "Heads" if user_choice == "heads" else "Tails"
        
        if won:
            status = "🎉 YOU WON!! 🎉"
            color = discord.Color.green()
        else:
            status = "❌ You Lost!"
            color = discord.Color.red()
        
        embed = discord.Embed(
            title=f"{emoji} Coin Flip!",
            description=f"You chose: **{choice_display}**\nThe coin landed on: **{result_display}**\n\n{status}",
            color=color
        )
        embed.set_image(url="https://cdn.nekotina.com/res/embeds/NyanCoinCat.gif")
        embed.set_footer(text=f"Flipped by {interaction.user.display_name}")
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="dice", description="Roll a dice!")
    @app_commands.describe(sides="Number of sides on the dice (default: 6)")
    async def dice(self, interaction: discord.Interaction, sides: int = 6):
        """Roll a dice with custom number of sides"""
        if sides < 2:
            await interaction.response.send_message("❌ The dice needs at least 2 sides!!", ephemeral=True)
            return
        
        if sides > 100:
            await interaction.response.send_message("❌ That's too many sides!! Max is 100!!", ephemeral=True)
            return
        
        result = random.randint(1, sides)
        
        embed = discord.Embed(
            title="🎲 Dice Roll!",
            description=f"You rolled a **{result}** on a {sides}-sided dice!",
            color=discord.Color.purple()
        )
        embed.set_footer(text=f"Rolled by {interaction.user.display_name}")
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="choose", description="Let me choose for you!")
    @app_commands.describe(choices="Separate your choices with commas (e.g., pizza, burger, sushi)")
    async def choose(self, interaction: discord.Interaction, choices: str):
        """Choose randomly from a list of options"""
        options = [choice.strip() for choice in choices.split(",") if choice.strip()]
        
        if len(options) < 2:
            await interaction.response.send_message(
                "❌ Please provide at least 2 choices separated by commas!!",
                ephemeral=True
            )
            return
        
        chosen = random.choice(options)
        
        embed = discord.Embed(
            title="🤔 I choose...",
            description=f"**{chosen}**!!",
            color=discord.Color.teal()
        )
        embed.add_field(name="Options were:", value=", ".join(options), inline=False)
        embed.set_footer(text=f"Chosen for {interaction.user.display_name}")
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="rate", description="Rate something from 0 to 10!")
    @app_commands.describe(thing="What do you want me to rate?")
    async def rate(self, interaction: discord.Interaction, thing: str):
        """Rate something with a random score"""
        rating = random.randint(0, 10)
        
        if rating >= 9:
            message = "omg amazing!! 💖✨"
            color = discord.Color.gold()
        elif rating >= 7:
            message = "pretty good!! >w<"
            color = discord.Color.green()
        elif rating >= 5:
            message = "it's okay i guess~ 😊"
            color = discord.Color.blue()
        elif rating >= 3:
            message = "ehh not great... 😅"
            color = discord.Color.orange()
        else:
            message = "oof... not good >w<"
            color = discord.Color.red()
        
        stars = "⭐" * rating + "☆" * (10 - rating)
        
        embed = discord.Embed(
            title=f"Rating: {thing}",
            description=f"{stars}\n\n**{rating}/10** - {message}",
            color=color
        )
        embed.set_footer(text=f"Rated for {interaction.user.display_name}")
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="reverse", description="Reverse your text!")
    @app_commands.describe(text="The text to reverse")
    async def reverse(self, interaction: discord.Interaction, text: str):
        """Reverse the input text"""
        reversed_text = text[::-1]
        
        embed = discord.Embed(
            title="🔄 Reversed Text",
            description=f"**Original:** {text}\n**Reversed:** {reversed_text}",
            color=discord.Color.purple()
        )
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="mock", description="MoCk YoUr TeXt LiKe ThIs!")
    @app_commands.describe(text="The text to mock")
    async def mock(self, interaction: discord.Interaction, text: str):
        """Convert text to mocking spongebob case"""
        mocked = ""
        for i, char in enumerate(text):
            if i % 2 == 0:
                mocked += char.lower()
            else:
                mocked += char.upper()
        
        class MockView(discord.ui.View):
            def __init__(self, mocked_text):
                super().__init__(timeout=60)
                self.mocked_text = mocked_text
            
            @discord.ui.button(label="✅ Yes", style=discord.ButtonStyle.success)
            async def yes_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                await interaction.response.send_message(self.mocked_text)
            
            @discord.ui.button(label="❌ No", style=discord.ButtonStyle.danger)
            async def no_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                await interaction.response.send_message("ight bet")
        
        message_content = f"{mocked}\n\n-# Mocked by {interaction.user.display_name}"
        
        view = MockView(mocked)
        await interaction.response.send_message(f"{message_content}\n\nCopy paste the text?", view=view, ephemeral=True)

    @app_commands.command(name="uwuify", description="Make your text more uwu!")
    @app_commands.describe(text="The text to uwuify")
    async def uwuify(self, interaction: discord.Interaction, text: str):
        """some uwu type shit replace"""
        uwu_text = text.replace("r", "w").replace("R", "W")
        uwu_text = uwu_text.replace("l", "w").replace("L", "W")
        uwu_text = uwu_text.replace("na", "nya").replace("Na", "Nya").replace("NA", "NYA")
        uwu_text = uwu_text.replace("ne", "nye").replace("Ne", "Nye").replace("NE", "NYE")
        uwu_text = uwu_text.replace("ni", "nyi").replace("Ni", "Nyi").replace("NI", "NYI")
        uwu_text = uwu_text.replace("no", "nyo").replace("No", "Nyo").replace("NO", "NYO")
        uwu_text = uwu_text.replace("nu", "nyu").replace("Nu", "Nyu").replace("NU", "NYU")
        
        # adding face for no reason
        emoticons = [" uwu", " owo", " >w<", " ^w^", " :3", " >///<"]
        if random.random() > 0.5:
            uwu_text += random.choice(emoticons)
        
        await interaction.response.send_message(f"{uwu_text}")

    @app_commands.command(name="ascii", description="Convert text to ASCII art!")
    @app_commands.describe(text="The text to convert (keep it short!)")
    async def ascii(self, interaction: discord.Interaction, text: str):
        """Convert text to ASCII art"""
        if len(text) > 10:
            await interaction.response.send_message(
                "❌ Text is too long!! Please keep it under 10 characters!!",
                ephemeral=True
            )
            return
        
        # Simple ASCII art mapping
        ascii_art = {
            'A': ['  A  ', ' A A ', 'AAAAA', 'A   A', 'A   A'],
            'B': ['BBBB ', 'B   B', 'BBBB ', 'B   B', 'BBBB '],
            'C': [' CCC ', 'C   C', 'C    ', 'C   C', ' CCC '],
            'D': ['DDDD ', 'D   D', 'D   D', 'D   D', 'DDDD '],
            'E': ['EEEEE', 'E    ', 'EEEE ', 'E    ', 'EEEEE'],
            'F': ['FFFFF', 'F    ', 'FFFF ', 'F    ', 'F    '],
            'G': [' GGG ', 'G    ', 'G  GG', 'G   G', ' GGG '],
            'H': ['H   H', 'H   H', 'HHHHH', 'H   H', 'H   H'],
            'I': ['IIIII', '  I  ', '  I  ', '  I  ', 'IIIII'],
            'J': ['JJJJJ', '    J', '    J', 'J   J', ' JJJ '],
            'K': ['K   K', 'K  K ', 'KKK  ', 'K  K ', 'K   K'],
            'L': ['L    ', 'L    ', 'L    ', 'L    ', 'LLLLL'],
            'M': ['M   M', 'MM MM', 'M M M', 'M   M', 'M   M'],
            'N': ['N   N', 'NN  N', 'N N N', 'N  NN', 'N   N'],
            'O': [' OOO ', 'O   O', 'O   O', 'O   O', ' OOO '],
            'P': ['PPPP ', 'P   P', 'PPPP ', 'P    ', 'P    '],
            'Q': [' QQQ ', 'Q   Q', 'Q   Q', 'Q  Q ', ' QQ Q'],
            'R': ['RRRR ', 'R   R', 'RRRR ', 'R  R ', 'R   R'],
            'S': [' SSS ', 'S    ', ' SSS ', '    S', ' SSS '],
            'T': ['TTTTT', '  T  ', '  T  ', '  T  ', '  T  '],
            'U': ['U   U', 'U   U', 'U   U', 'U   U', ' UUU '],
            'V': ['V   V', 'V   V', 'V   V', ' V V ', '  V  '],
            'W': ['W   W', 'W   W', 'W W W', 'WW WW', 'W   W'],
            'X': ['X   X', ' X X ', '  X  ', ' X X ', 'X   X'],
            'Y': ['Y   Y', ' Y Y ', '  Y  ', '  Y  ', '  Y  '],
            'Z': ['ZZZZZ', '   Z ', '  Z  ', ' Z   ', 'ZZZZZ'],
            ' ': ['     ', '     ', '     ', '     ', '     '],
        }
        
        lines = ['', '', '', '', '']
        for char in text.upper():
            if char in ascii_art:
                for i in range(5):
                    lines[i] += ascii_art[char][i] + ' '
        
        result = '\n'.join(lines)
        
        await interaction.response.send_message(f"```\n{result}\n```")

    @app_commands.command(name="emojify", description="Convert text to emojis!")
    @app_commands.describe(text="The text to emojify")
    async def emojify(self, interaction: discord.Interaction, text: str):
        """Convert text to regional indicator emojis"""
        emoji_map = {
            'a': '🇦', 'b': '🇧', 'c': '🇨', 'd': '🇩', 'e': '🇪', 'f': '🇫',
            'g': '🇬', 'h': '🇭', 'i': '🇮', 'j': '🇯', 'k': '🇰', 'l': '🇱',
            'm': '🇲', 'n': '🇳', 'o': '🇴', 'p': '🇵', 'q': '🇶', 'r': '🇷',
            's': '🇸', 't': '🇹', 'u': '🇺', 'v': '🇻', 'w': '🇼', 'x': '🇽',
            'y': '🇾', 'z': '🇿', ' ': '  '
        }
        
        emojified = ''.join(emoji_map.get(char.lower(), char) for char in text)
        
        if len(emojified) > 2000:
            await interaction.response.send_message(
                "❌ Text is too long to emojify!!",
                ephemeral=True
            )
            return
        
        await interaction.response.send_message(emojified)

    @app_commands.command(name="rps", description="Rock, Paper, Scissors!")
    @app_commands.describe(choice="Your choice: rock, paper, or scissors")
    async def rps(self, interaction: discord.Interaction, choice: str):
        choices = ["rock", "paper", "scissors"]
        bot_choice = random.choice(choices)
        if choice.lower() not in choices:
            await interaction.response.send_message("Choose rock, paper, or scissors!", ephemeral=True)
            return
        result = "It's a tie!" if choice.lower() == bot_choice else (
            "You win!" if (choice.lower() == "rock" and bot_choice == "scissors") or
                          (choice.lower() == "paper" and bot_choice == "rock") or
                          (choice.lower() == "scissors" and bot_choice == "paper")
            else "You lose!"
        )
        await interaction.response.send_message(f'I chose {bot_choice}. {result}')

async def setup(bot):
    await bot.add_cog(FunCommands(bot))
