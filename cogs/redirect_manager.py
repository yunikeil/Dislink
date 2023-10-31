import nextcord
from nextcord import Interaction, Locale
from nextcord.ext import tasks, application_checks
from nextcord.ext.commands import Bot, Cog

class RedirManagerCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.on_init.start()

    @tasks.loop(count=1)
    async def on_init(self):
        await self.bot.sync_all_application_commands()

    def cog_unload(self):
        pass

    @nextcord.slash_command(
        name="get_invite",
        name_localizations={
            Locale.en_US: "get_invite",
            Locale.ru: "получить_приглашение",
        },
        description_localizations={
            Locale.en_US: "Get an invite"
        },
        guild_ids=[1064192306904846377]
    )
    #@application_checks.has_permissions(administrator=True)
    async def get_invite(self, interaction: Interaction):
        print(interaction.locale)
        await interaction.response.send_message("123", ephemeral=True)

    @nextcord.slash_command(
        name="create_invite",
        name_localizations={
            Locale.en_US: "create_invite",
            Locale.ru: "создать_приглашение",
        },
        description_localizations={
            Locale.en_US: "Create an invite"
        },
        guild_ids=[1064192306904846377]
    )
    #@application_checks.has_permissions(administrator=True)
    async def create_invite(self, interaction: Interaction):
        await interaction.response.send_message("123", ephemeral=True)

    @nextcord.slash_command(
        name="update_invite",
        name_localizations={
            Locale.en_US: "update_invite",
            Locale.ru: "обновить_приглашение",
        },
        description_localizations={
            Locale.en_US: "Update an invite",
        },
        guild_ids=[1064192306904846377]
    )
    #@application_checks.has_permissions(administrator=True)
    async def update_invite(self, interaction: Interaction):
        await interaction.response.send_message("123", ephemeral=True)

    @nextcord.slash_command(
        name="delete_invite",
        name_localizations={
            Locale.en_US: "delete_invite",
            Locale.ru: "удалить_приглашение",
        },
        description_localizations={
            Locale.en_US: "Delete an invite",
        },
        guild_ids=[1064192306904846377]
    )
    #@application_checks.has_permissions(administrator=True)
    async def delete_invite(self, interaction: Interaction):
        await interaction.response.send_message("123", ephemeral=True)

def setup(bot: Bot):
    print("RedirManagerCog loaded!")
    bot.add_cog(RedirManagerCog(bot))
