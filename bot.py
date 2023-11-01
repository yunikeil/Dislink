import asyncio
import logging

import aeval
import discord
from discord import app_commands
from discord.ext import commands

import configuration


class DeleteMessage(discord.ui.View):
    def __init__(self, *, message, ctx):
        super().__init__(timeout=60 * 5)
        self.message = message
        self.ctx = ctx

    @discord.ui.button(label="delete this message", style=discord.ButtonStyle.grey)
    async def delete_this(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        if self.ctx.author.id == interaction.user.id:
            await interaction.message.delete()

    @discord.ui.button(label="delete two messages", style=discord.ButtonStyle.grey)
    async def delete_two(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        if self.ctx.author.id == interaction.user.id:
            await self.ctx.message.delete()
            await interaction.message.delete()

    async def on_timeout(self):
        self.delete_this.disabled = True
        self.delete_two.disabled = True
        try:
            await self.message.edit(view=self)
        except BaseException:
            pass


class Bot(commands.Bot):
    def __init__(
        self,
        cogs_add_on_ready=None,
        command_prefix=None,
        help_command=None,
        intents=None,
    ):
        super().__init__(
            command_prefix=command_prefix, help_command=help_command, intents=intents
        )
        self.DATA: dict = {"bot-started": False}
        self.OWNERS = configuration.bot_owners
        self.EVAL_OWNER = configuration.eval_owners
        self.cogs_add_on_ready = cogs_add_on_ready
    
    async def setup_hook(self):
        if self.cogs_add_on_ready:
            [
                await self.load_extension(f"cogs.{cog}")
                for cog in self.cogs_add_on_ready
            ]
        self.tree.copy_global_to(guild=discord.Object(id=1064192306904846377))
        await self.tree.sync()

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})\n------")
        if not self.DATA["bot-started"]:
            application_info = await self.application_info()
            self.OWNERS.append(application_info.owner.id)
            self.EVAL_OWNER.append(application_info.owner.id)
            self.DATA["bot-started"] = True

intents = discord.Intents.default()
intents.message_content = True  

bot: commands.Bot = Bot(
    cogs_add_on_ready=configuration.cogs_add_on_ready,
    intents=intents,
    command_prefix=">",
    help_command=None,
)


@bot.command()
async def cog_load(ctx: commands.Context, cog: str):
    if ctx.author.id not in bot.OWNERS:
        return
    try:
        await bot.load_extension(f"cogs.{cog}")
    except BaseException as ex:
        message = await ctx.channel.send(f"Exception:\n```bash\n{ex}\n```")
        await message.edit(view=DeleteMessage(ctx=ctx, message=message))
    else:
        message = await ctx.channel.send(f"```cogs.{cog} loaded!```")
        await message.edit(view=DeleteMessage(ctx=ctx, message=message))


@bot.command()
async def cog_unload(ctx: commands.Context, cog: str):
    if ctx.author.id not in bot.OWNERS:
        return
    try:
        await bot.unload_extension(f"cogs.{cog}")
    except BaseException as ex:
        message = await ctx.channel.send(f"Exception:\n```bash\n{ex}\n```")
        await message.edit(view=DeleteMessage(ctx=ctx, message=message))
    else:
        message = await ctx.channel.send(f"```cogs.{cog} unloaded!```")
        await message.edit(view=DeleteMessage(ctx=ctx, message=message))


@bot.command()
async def cog_reload(ctx: commands.Context, cog: str):
    if ctx.author.id not in bot.OWNERS:
        return
    try:
        await bot.reload_extension(f"cogs.{cog}")
    except BaseException as ex:
        message = await ctx.channel.send(f"Exception:\n```bash\n{ex}\n```")
        await message.edit(view=DeleteMessage(ctx=ctx, message=message))
    else:
        message = await ctx.channel.send(f"```cogs.{cog} reloaded!```")
        await message.edit(view=DeleteMessage(ctx=ctx, message=message))


@bot.command()
async def remove_cog(ctx: commands.Context, cog: str):
    if ctx.author.id not in bot.OWNERS:
        return
    try:
        await bot.remove_cog(name=f"{cog}")
    except BaseException as ex:
        message = await ctx.channel.send(f"Exception:\n```bash\n{ex}\n```")
        await message.edit(view=DeleteMessage(ctx=ctx, message=message))
    else:
        message = await ctx.channel.send(f"```cogs.{cog} removed!```")
        await message.edit(view=DeleteMessage(ctx=ctx, message=message))


@bot.command(name="eval")
async def eval_string(ctx, *, content):
    if ctx.author.id not in bot.EVAL_OWNER:
        return
    standart_args = {
        "discord": discord,
        "commands": commands,
        "bot": bot,
        "ctx": ctx,
        "asyncio": asyncio,
    }
    if "```" in content:
        content = "\n".join(content.split("\n")[1:-1])
    try:
        await aeval.aeval(content, standart_args, {})
    except Exception as ex:
        message = await ctx.channel.send(
            f"Exception:\n```bash\n{str(ex).replace('```', '`')}\n```"
        )
        await message.edit(view=DeleteMessage(ctx=ctx, message=message))


if __name__ == "__main__":
    bot.run(configuration.discord_token)
