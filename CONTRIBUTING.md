# Contributing to WeebOwO Bot 🎀

Thank you for considering contributing to WeebOwO Bot! We love to receive contributions from the community.

## How to Contribute

### Reporting Bugs 🐛

If you find a bug, please create an issue with:
- A clear title and description
- Steps to reproduce the bug
- Expected vs actual behavior
- Screenshots if applicable
- Your Python and discord.py version

### Suggesting Features ✨

We're always open to new ideas! When suggesting a feature:
- Check if it's already been suggested
- Explain why this feature would be useful
- Provide examples of how it would work

### Pull Requests 🔧

1. **Fork the repository**
2. **Create a new branch** for your feature
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
   - Follow the existing code style
   - Add comments where necessary
   - Test your changes thoroughly
4. **Commit your changes**
   ```bash
   git commit -m "Add amazing feature"
   ```
5. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```
6. **Open a Pull Request**

## Code Style Guidelines 📝

### Python Code
- Follow PEP 8 style guide
- Use meaningful variable and function names
- Add docstrings to functions
- Keep functions focused and small

### Cogs Structure
All commands should be organized in cogs:
```python
import discord
from discord.ext import commands
from discord import app_commands

class MyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mycommand", description="Description here")
    async def mycommand(self, interaction: discord.Interaction):
        await interaction.response.send_message("Hello!")

async def setup(bot):
    await bot.add_cog(MyCog(bot))
```

### Command Guidelines
- Use slash commands (`@app_commands.command`) for new features
- Add clear descriptions and parameter hints
- Handle errors gracefully
- Use ephemeral messages for error/info messages
- Add appropriate permission checks

### Commit Messages
- Use clear, descriptive commit messages
- Start with a verb (Add, Fix, Update, Remove)
- Examples:
  - `Add /hug command with GIF support`
  - `Fix music queue not clearing properly`
  - `Update help command with new features`

## Testing 🧪

Before submitting a PR:
- Test your changes in a real Discord server
- Make sure existing commands still work
- Check for any Python errors or warnings
- Test edge cases (empty inputs, invalid data, etc.)

## Questions? 💬

If you have questions about contributing:
- Join our Discord: [discord.gg/3knu2FNqDG](https://discord.gg/3knu2FNqDG)
- Contact Weebo64: <@257196097494188032>

## Code of Conduct 🤝

- Be respectful and inclusive
- Help others learn and grow
- Give constructive feedback
- Have fun! This is a community project :3

Thank you for contributing! 💖
