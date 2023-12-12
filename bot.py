import logging

import discord
from discord import app_commands
from discord.ext import commands

import core.settings as configuration


class MyCustomTranslator(app_commands.Translator):
    async def load(self):
        ...
    # this gets called when the translator first gets loaded!
    async def unload(self):
        ...
        # in case you need to switch translators, this gets called when being removed
    async def translate(self, string: app_commands.locale_str, locale: discord.Locale, context: app_commands.TranslationContext):
        """
        `locale_str` is the string that is requesting to be translated
        `locale` is the target language to translate to
        `context` is the origin of this string, eg TranslationContext.command_name, etc
        This function must return a string (that's been translated), or `None` to signal no available translation available, and will default to the original.
        """
        return string.message


class Bot(commands.Bot):
    def __init__(
        self,
        command_prefix=None,
        help_command=None,
        intents=None,
        cogs_on_start=None,
        **kwargs,
    ):
        super().__init__(
            command_prefix=command_prefix,
            help_command=help_command,
            intents=intents,
            **kwargs,
        )
        self.DATA: dict = {"bot-started": False}
        self.OWNERS = configuration.bot_owners
        self.EVAL_OWNER = configuration.eval_owners
        self.cogs_on_start = cogs_on_start

    async def setup_hook(self):
        await self.tree.set_translator(MyCustomTranslator())
        if self.cogs_on_start:
            [await self.load_extension(f"cogs.{cog}") for cog in self.cogs_on_start]
        #self.tree.copy_global_to(guild=discord.Object(id=1064192306904846377))
        #await self.tree.sync(guild=discord.Object(id=1064192306904846377))

    async def on_ready(self):
        logging.getLogger("discord.client") \
            .info(f"Logged in as {self.user} (ID: {self.user.id}")
        if not self.DATA["bot-started"]:
            application_info = await self.application_info()
            self.OWNERS.append(application_info.owner.id)
            self.EVAL_OWNER.append(application_info.owner.id)
            self.DATA["bot-started"] = True


intents = discord.Intents.default()
bot: commands.Bot = Bot(
    command_prefix=">",
    cogs_on_start=configuration.cogs_on_start,
    intents=intents,
    status=discord.Status.dnd
)





if __name__ == "__main__":
    bot.run(configuration.discord_token)
