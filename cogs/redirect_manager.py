import logging
from requests.models import Response
from contextlib import asynccontextmanager

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.app_commands import locale_str as _T


@asynccontextmanager
async def requests_error_handler(interaction: discord.Interaction):
    try:
        yield
    except aiohttp.ClientConnectionError:
        await interaction.response.send_message(_T("api_unavailable"))
    except:
        await interaction.response.send_message(_T("unknown_error"))


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
    @app_commands.guild_only
    @app_commands.default_permissions(administrator=True)
    @app_commands.guilds(1169354124299603978)  # Temp decorator
    @app_commands.rename(channel='channel')
    @app_commands.rename(domen_link='domen_link')
    @app_commands.describe(channel='channel_discr')
    @app_commands.describe(domen_link='domen_link_discr')
    async def create_shortcut(
        self,
        interaction: discord.Interaction,
        channel: discord.abc.GuildChannel,
        domen_link: str,
    ) -> None:
        invite = await channel.create_invite(
            reason=f"{interaction.user.name} used /{_T('create_shortcut_name')}",
            max_age=0,
        )
        async with requests_error_handler(interaction):
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url=f"{api_url}/redirect",
                    json={
                        "server_id": interaction.guild_id,
                        "server_link": invite.code,
                        "domen_link": domen_link,
                    },
                ) as resp:
                    response: dict = await resp.json()

                    if resp.status == 200:
                        await interaction.response.send_message(
                            f"Link created: [dislink.space/{response.get('domen_link')}]"
                            f"(https://discord.gg/{response.get('server_link')} )",
                            ephemeral=True,
                        )
                    elif resp.status == 403:
                        await interaction.response.send_message(
                            f"{response.get('detail')}", ephemeral=True
                        )
                    else:
                        await interaction.response.send_message(
                            _T("unknown_error"), ephemeral=True
                        )

    @app_commands.command(
        name=_T("get_shortcut_name"), description=_T("get_shortcut_description")
    )
    @app_commands.guilds(1064192306904846377)  # Temp decorator
    async def get_shortcut(self, interaction: discord.Interaction) -> None:
        async with requests_error_handler(interaction):
            async with aiohttp.ClientSession() as session:  
                ...

        await interaction.response.send_message("Shortcut retrieved!", ephemeral=True)

    @app_commands.command(
        name=_T("update_shortcut_name"), description=_T("update_shortcut_description")
    )
    @app_commands.guilds(1064192306904846377)  # Temp decorator
    async def update_shortcut(self, interaction: discord.Interaction) -> None:
        async with requests_error_handler(interaction):
            async with aiohttp.ClientSession() as session:
                ...

        await interaction.response.send_message("Shortcut updated!", ephemeral=True)

    @app_commands.command(
        name=_T("delete_shortcut_name"), description=_T("delete_shortcut_description")
    )
    @app_commands.guilds(1064192306904846377)  # Temp decorator
    async def delete_shortcut(self, interaction: discord.Interaction) -> None:
        async with requests_error_handler(interaction):
            async with aiohttp.ClientSession() as session:
                ...

        await interaction.response.send_message("Shortcut deleted!", ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    logging.getLogger("discord.cogs.load").info("RedirectCog loaded!")
    await bot.add_cog(RedirectCog(bot))
