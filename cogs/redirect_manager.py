import logging
import requests

import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.app_commands import locale_str as _T

from configuration import api_url

class RedirectCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        print(type(self.create_shortcut))
        self.on_init.start()

    @tasks.loop(count=1)
    async def on_init(self):
        pass

    @app_commands.command(
        name=_T("create_shortcut_name"), description=_T("create_shortcut_description")
    )
    @app_commands.guilds(1064192306904846377)  # Temp decorator
    async def create_shortcut(self, interaction: discord.Interaction, channel: discord.abc.GuildChannel, domen_link: str) -> None:
        invite = await channel.create_invite(reason=f"{interaction.user.name} used /{_T('create_shortcut_name')}")
        try:
            response = requests.post(
                url = f"{api_url}/redirect",
                json = {"server_id": interaction.guild_id, "server_link": invite.code, "domen_link": domen_link}
            ).json()
        except requests.exceptions.ConnectionError as e:
            await interaction.response.send_message("Api server not unavailable")

        await interaction.response.send_message(f"Shortcut created!\n```json\n{response}```", ephemeral=True)

    @app_commands.command(
        name=_T("get_shortcut_name"), description=_T("get_shortcut_description")
    )
    @app_commands.guilds(1064192306904846377)  # Temp decorator
    async def get_shortcut(self, interaction: discord.Interaction) -> None:
        #response = requests.get(f"{api_url}/redirect")

        await interaction.response.send_message("Shortcut retrieved!", ephemeral=True)

    @app_commands.command(
        name=_T("update_shortcut_name"), description=_T("update_shortcut_description")
    )
    @app_commands.guilds(1064192306904846377)  # Temp decorator
    async def update_shortcut(self, interaction: discord.Interaction) -> None:
        #response = requests.put(f"{api_url}/redirect")
        

        await interaction.response.send_message("Shortcut updated!", ephemeral=True)

    @app_commands.command(
        name=_T("delete_shortcut_name"), description=_T("delete_shortcut_description")
    )
    @app_commands.guilds(1064192306904846377)  # Temp decorator
    async def delete_shortcut(self, interaction: discord.Interaction) -> None:
        #response = requests.delete(f"{api_url}/redirect")
        

        await interaction.response.send_message("Shortcut deleted!", ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    logging.getLogger("discord.cogs.load").info("RedirectCog loaded!")
    await bot.add_cog(RedirectCog(bot))
