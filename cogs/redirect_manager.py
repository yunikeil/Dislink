import logging
from typing import Tuple, Any
from contextlib import asynccontextmanager

import aiohttp
from aiohttp import ClientResponse
import discord
from discord import app_commands
from discord.ext import commands
from discord.app_commands import locale_str as _T


@asynccontextmanager
async def requests_error_handler(interaction: discord.Interaction):
    errors = []  # Container to store errors
    try:
        yield errors
    except aiohttp.ClientConnectionError:
        errors.append("api_unavailable")
    except aiohttp.client_exceptions.ContentTypeError:
        errors.append("api_unavailable")
    except BaseException as e:
        errors.append("unknown_error")


class RedirectCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @staticmethod
    async def create_redirect(interaction, *, server_id, server_link, domen_link) -> Tuple[dict, Any]:
        async with requests_error_handler(interaction) as errors:
            url = f"https://dislink.space/c/redirect"
            data = {"server_id": server_id, "server_link": server_link, "domen_link": domen_link}
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=data) as response:
                    status = response.status
                    response = await response.json()
        return status, response, errors[0] if errors else None

    @staticmethod
    async def get_redirect(interaction, *, server_id) -> Tuple[dict, Any]:
        async with requests_error_handler(interaction) as errors:
            url = f"https://dislink.space/c/redirect"
            params = {'server_id': server_id}
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    status = response.status
                    response = await response.json()
        return status, response, errors[0] if errors else None
            
    @staticmethod
    async def update_redirect(interaction, *, server_id: int, server_link: str | None = None, domen_link: str | None = None) -> Tuple[dict, Any]:
        async with requests_error_handler(interaction) as errors:
            url = f"https://dislink.space/c/redirect"
            params = {'server_id': server_id}
            data = {"server_link": server_link, "domen_link": domen_link}
            
            if not data.get("server_link"):
                del data["server_link"]
            
            if not data.get("domen_link"):
                del data["domen_link"]
            
            async with aiohttp.ClientSession() as session:
                async with session.put(url, json=data, params=params) as response:
                    status = response.status
                    response = await response.json()
        return status, response, errors[0] if errors else None

    @staticmethod
    async def delete_redirect(interaction, *, server_id) -> Tuple[dict, Any]:
        async with requests_error_handler(interaction) as errors:
            url = f"https://dislink.space/c/redirect"
            params = {'server_id': server_id}
            async with aiohttp.ClientSession() as session:
                async with session.delete(url, params=params) as response:
                    status = response.status
                    response = await response.json()
        return status, response, errors[0] if errors else None
        
    @app_commands.command(
        name=_T("create_shortcut_name"), description=_T("create_shortcut_description")
    )
    @app_commands.default_permissions(administrator=True)
    @app_commands.guilds(1064192306904846377)
    async def create_shortcut(
        self,
        interaction: discord.Interaction,
        channel: discord.abc.GuildChannel,
        domen_link: str,
    ) -> None:
        """
        {'server_link': 'nK7QTt7bw9', 'domen_link': 'test', 'updated_at': 1702403522, 'server_id': 1064192306904846377, 'last_use': 1702403522, 'created_at': 1702403522}
        """
        invite = await channel.create_invite(
            reason=f"{interaction.user.name} used /{_T('create_shortcut_name')}",
            max_age=0,
        )
        status, response, server_error = await self.create_redirect(interaction, server_id=interaction.guild_id, server_link=invite.code, domen_link=domen_link)
        
        if server_error:
            await interaction.response.send_message(
                content=_T(server_error), ephemeral=True
            )
            return
        
        if not response:
            await interaction.response.send_message(
                content=_T("unknown_error"), ephemeral=True
            )
            return
            
        match status:
            case 200:
                # TODO embed response
                await interaction.response.send_message(
                    content=response
                )
            case 409:
                await interaction.response.send_message(
                    content=_T(response)
                )
            
    @app_commands.command(
        name=_T("get_shortcut_name"), description=_T("get_shortcut_description")
    )
    @app_commands.guilds(1064192306904846377)  # Temp decorator
    async def get_shortcut(self, interaction: discord.Interaction) -> None:
        status, response, server_error = await self.get_redirect(interaction, server_id=interaction.guild_id)
        """
        {'server_link': 'nK7QTt7bw9', 'domen_link': 'test', 'updated_at': 1702403522, 'server_id': 1064192306904846377, 'last_use': 1702403522, 'created_at': 1702403522}
        """
        if server_error:
            await interaction.response.send_message(
                content=_T(server_error), ephemeral=True
            )
            return
        
        if not response:
            await interaction.response.send_message(
                content=_T("unknown_error"), ephemeral=True
            )
            return
            
        match status:
            case 200:
                # TODO embed response
                await interaction.response.send_message(
                    content=response
                )
            case 404:
                await interaction.response.send_message(
                    content=_T(response)
                )
    
    @app_commands.command(
        name=_T("update_shortcut_name"), description=_T("update_shortcut_description")
    )
    @app_commands.guilds(1064192306904846377)  # Temp decorator
    async def update_shortcut(self, interaction: discord.Interaction, domen_link: str) -> None:
        status, response, server_error = await self.update_redirect(interaction, server_id=interaction.guild_id, domen_link=domen_link)
        
        if server_error:
            await interaction.response.send_message(
                content=_T(server_error), ephemeral=True
            )
            return
        
        if not response:
            await interaction.response.send_message(
                content=_T("unknown_error"), ephemeral=True
            )
            return
            
        match status:
            case 200:
                # TODO embed response
                await interaction.response.send_message(
                    content=response
                )
            case 404:
                await interaction.response.send_message(
                    content=_T(response)
                )
            case 409:
                await interaction.response.send_message(
                    content=_T(response)
                )    
    
    @app_commands.command(
        name=_T("delete_shortcut_name"), description=_T("delete_shortcut_description")
    )
    @app_commands.guilds(1064192306904846377)  # Temp decorator
    async def delete_shortcut(self, interaction: discord.Interaction) -> None:
        # TODO удаление приглашения
        status, response, server_error = await self.delete_redirect(interaction, server_id=interaction.guild_id)
        
        if server_error:
            await interaction.response.send_message(
                content=_T(server_error), ephemeral=True
            )
            return
        
        if not response:
            await interaction.response.send_message(
                content=_T("unknown_error"), ephemeral=True
            )
            return
            
        match status:
            case 200:
                # TODO embed response
                await interaction.response.send_message(
                    content=response
                )
            case 404:
                await interaction.response.send_message(
                    content=_T(response)
                )
    
    @commands.Cog.listener()
    async def on_invite_delete(self, invite: discord.Invite):
        # TODO Удаление записи на сервере
        print(f'Приглашение {invite.code} было удалено.')

async def setup(bot: commands.Bot) -> None:
    logging.getLogger("discord.cogs.load").info("RedirectCog loaded!")
    await bot.add_cog(RedirectCog(bot))
