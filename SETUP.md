# Setup Guide for WeebOwO Bot 🚀

## Quick Start (Windows)

### 1. Install Python
- Download Python 3.8+ from [python.org](https://www.python.org/downloads/)
- ✅ Check "Add Python to PATH" during installation
- Verify installation:
  ```cmd
  python --version
  ```

### 2. Install FFmpeg (Required for Music)
- Download from [gyan.dev/ffmpeg](https://www.gyan.dev/ffmpeg/builds/)
- Extract to `C:\ffmpeg`
- Add to PATH:
  1. Search "Environment Variables" in Windows
  2. Edit "Path" under System Variables
  3. Add `C:\ffmpeg\bin`
- Verify:
  ```cmd
  ffmpeg -version
  ```

### 3. Clone/Download the Bot
```cmd
git clone https://github.com/yourusername/weebowo-bot.git
cd weebowo-bot
```

Or download as ZIP and extract.

### 4. Install Dependencies
```cmd
pip install -r requirements.txt
```

### 5. Configure Environment Variables
1. Copy `.env.example` to `.env`
2. Edit `.env` with your tokens:

```env
DISCORD_TOKEN=your_bot_token_here
TENOR_API_KEY=your_tenor_key_here
```

#### Getting Your Discord Token:
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application"
3. Go to "Bot" tab
4. Click "Reset Token" and copy it
5. Enable these intents:
   - ✅ Presence Intent
   - ✅ Server Members Intent
   - ✅ Message Content Intent

#### Getting Tenor API Key:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable "Tenor API"
4. Create credentials (API Key)
5. Copy the key

### 6. Add WeebOwO Images (Optional)
- Create a `WeebOwO` folder
- Add your WeebOwO images (PNG, JPG, GIF)
- These will be used for `/weebowo` command

### 7. Run the Bot
```cmd
python bot.py
```

You should see:
```
✅ Bot is online! Logged in as WeebOwO#1234
🌐 WeebOwO is in X servers:
```

### 8. Invite Bot to Your Server
1. Go to Discord Developer Portal
2. OAuth2 → URL Generator
3. Select scopes:
   - ✅ bot
   - ✅ applications.commands
4. Select permissions:
   - ✅ Send Messages
   - ✅ Manage Messages
   - ✅ Embed Links
   - ✅ Attach Files
   - ✅ Read Message History
   - ✅ Add Reactions
   - ✅ Connect (for voice)
   - ✅ Speak (for voice)
   - ✅ Kick Members (optional)
   - ✅ Ban Members (optional)
   - ✅ Manage Channels (optional)
5. Copy the generated URL and open it in your browser

## Troubleshooting 🔧

### "discord.py not found"
```cmd
pip install discord.py
```

### "FFmpeg not found"
- Make sure FFmpeg is in PATH
- Restart your terminal after adding to PATH

### "Bot doesn't respond to commands"
- Check if bot is online in Discord
- Make sure Message Content Intent is enabled
- Run `/help` to test slash commands

### "Permission denied" errors
- Check bot permissions in Discord server
- Make sure bot role is high enough in role hierarchy

## Running 24/7 (Optional)

### Using a VPS/Server
1. Upload bot files to server
2. Install dependencies
3. Use `screen` or `tmux` to keep bot running:
   ```bash
   screen -S weebowo
   python bot.py
   # Press Ctrl+A then D to detach
   ```

### Using a Hosting Service
- [Railway.app](https://railway.app/)
- [Heroku](https://www.heroku.com/)
- [Replit](https://replit.com/)

## Need Help? 💬

- Join Discord: [discord.gg/3knu2FNqDG](https://discord.gg/3knu2FNqDG)
- Contact: <@257196097494188032>
- Check `#help-about-the-bot` channel

---

Have fun with your bot! 💖
