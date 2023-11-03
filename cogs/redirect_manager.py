import logging
import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.app_commands import locale_str as _T

class MyCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        print(type(self.create_shortcut))
        self.on_init.start()

    @tasks.loop(count=1)
    async def on_init(self):
        pass

    @app_commands.command(name=_T("create-shortcut"))
    @app_commands.guilds(1064192306904846377)
    async def create_shortcut(self, interaction: discord.Interaction) -> None:
        # Здесь вы можете добавить код для создания сокращения
        await interaction.response.send_message("Shortcut created!", ephemeral=True)

    @app_commands.command(name="get-shortcut")
    @app_commands.guilds(1064192306904846377)
    async def get_shortcut(self, interaction: discord.Interaction) -> None:
        # Здесь вы можете добавить код для получения сокращения
        await interaction.response.send_message("Shortcut retrieved!", ephemeral=True)

    @app_commands.command(name="update-shortcut")
    @app_commands.guilds(1064192306904846377)
    async def update_shortcut(self, interaction: discord.Interaction) -> None:
        # Здесь вы можете добавить код для обновления сокращения
        await interaction.response.send_message("Shortcut updated!", ephemeral=True)

    @app_commands.command(name="delete-shortcut")
    @app_commands.guilds(1064192306904846377)
    async def delete_shortcut(self, interaction: discord.Interaction) -> None:
        # Здесь вы можете добавить код для удаления сокращения
        await interaction.response.send_message("Shortcut deleted!", ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    logging.getLogger('discord.load.cogs').info("MyCog loaded!")
    await bot.add_cog(MyCog(bot))
