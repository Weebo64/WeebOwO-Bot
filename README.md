# WeebOwO Discord Bot 🎀

A fun and feature-rich Discord bot created by [Weebo64](https://weebo64.is-a.dev/) with lots of silly and useful commands!

## Features ✨

### 🎮 Fun Commands
- `/weebowo` - Random cute WeebOwO images (Art by kytronix & funnyhoohooman)
- `/cinema` - Absolute cinema meme
- `/pat`, `/kiss`, `/slap`, `/poke`, `/bonk`, `/hug` - Interaction commands with anime GIFs
- `/ship` - Ship two users together with compatibility
- `/8ball` - Magic 8-ball
- `/car` - Random cat GIFs
- `/coinflip`, `/dice`, `/rps` - Games
- `/choose`, `/rate` - Decision making
- Text manipulation: `/color`, `/reverse`, `/mock`, `/uwuify`, `/ascii`, `/emojify`

### 🎵 Music & Media
- `!play <url>` - Play YouTube or Spotify audio
- `/music <file>` - Upload and play custom audio files
- `/queue`, `/skip`, `/pause`, `/resume`, `/stop` - Playback controls
- `!loop` - Loop current song
- `/download_mp3` - Download YouTube audio
- `/embed_video` - Download Instagram, TikTok, or Twitter/X videos

### 👮 Moderation
- `/ban`, `/kick` - Member management
- `/warn`, `/remove_warnings`, `/show_warning` - Warning system
- `/purge` - Bulk delete messages
- `/slowmode` - Set channel slowmode
- `/lock`, `/unlock` - Channel locking
- Automod with banned words filter

### ℹ️ Utility
- `/help` - Command list
- `/ping` - Check latency
- `/userinfo`, `/serverinfo` - Server information
- `/avatar` - View user avatars
- `/afk` - AFK system
- `/remindme` - Set reminders
- `/say`, `/say_in`, `/reply` - Message commands

### 🎮 Mario Kart Wii
- `/setfc` - Add your friend code
- `/fc` - View friend codes

## Installation 🚀

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- A Discord Bot Token

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/weebowo-bot.git
cd weebowo-bot
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**
   - Copy `.env.example` to `.env`
   - Fill in your tokens:
```env
DISCORD_TOKEN=your_discord_bot_token_here
TENOR_API_KEY=your_tenor_api_key_here
OPENAI_API_KEY=your_openai_api_key_here  # Optional
```

4. **Get your API keys**
   - **Discord Token**: [Discord Developer Portal](https://discord.com/developers/applications)
   - **Tenor API Key**: [Google Tenor API](https://developers.google.com/tenor/guides/quickstart)
   - **OpenAI API Key** (optional): [OpenAI Platform](https://platform.openai.com/api-keys)

5. **Run the bot**
```bash
python bot.py
```

## Project Structure 📁

```
weebowo-bot/
├── bot.py                 # Main bot file
├── cogs/                  # Command modules
│   ├── fun_commands.py    # Fun interaction commands
│   ├── images.py          # Image/GIF commands
│   ├── music.py           # Music playback
│   ├── moderation.py      # Moderation tools
│   ├── utility.py         # Utility commands
│   ├── welcome.py         # Event handlers
│   ├── mario_kart.py      # Mario Kart friend codes
│   ├── youtube_downloader.py
│   ├── afk_system.py
│   ├── automod.py
│   └── ...
├── WeebOwO/              # WeebOwO image folder
├── uploads/              # Music uploads
├── .env                  # Environment variables (not in repo)
├── .env.example          # Example environment file
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Configuration ⚙️

### Required Folders
The bot will automatically create these folders if they don't exist:
- `uploads/` - For uploaded music files
- `WeebOwO/` - Add your WeebOwO images here for the `/weebowo` command

### Banned Words
Edit `cogs/banned_words.txt` to add words for the automod filter (one per line).

## Contributing 🤝

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## Credits 💖

- **Bot Creator**: [Weebo64](https://weebo64.is-a.dev/)
- **WeebOwO Art**: kytronix & funnyhoohooman
- **Special Thanks**: 
  - All contributors and supporters
  - Everyone who uses this bot!

## Support 💬

If you have any issues or questions:
- Contact <@257196097494188032> on Discord
- Join the support server: [discord.gg/3knu2FNqDG](https://discord.gg/3knu2FNqDG)
- Check `#help-about-the-bot` channel

## Terms of Service 📜

- [Terms of Service](https://pastebin.com/eCk6W69N)
- [Privacy Policy](https://pastebin.com/V8Vqdnkb)

## License 📄

This project is open source. Feel free to use and modify it for your own Discord bot!

---

Made with 💖 by Weebo64 | [Website](https://weebo64.is-a.dev/) | [Twitter](https://x.com/weebo64)
