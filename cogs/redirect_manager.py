import logging

import discord
from discord import app_commands
from discord.ext import commands, tasks


class MyCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.on_init.start()

    @tasks.loop(count=1)
    async def on_init(self):
        pass

    @app_commands.command(name="command-1")
    async def my_command(self, interaction: discord.Interaction) -> None:
        """ /command-1 """
        await interaction.response.send_message("Hello from command 1!", ephemeral=True)

    @app_commands.command(name="command-2")
    @app_commands.guilds(1064192306904846377)
    async def my_private_command(self, interaction: discord.Interaction) -> None:
        """ /command-2 """
        await interaction.response.send_message("Hello from private command!", ephemeral=True)

async def setup(bot: commands.Bot) -> None:
    logging.getLogger('discord.load.cogs').info("MyCog loaded!")
    await bot.add_cog(MyCog(bot))
