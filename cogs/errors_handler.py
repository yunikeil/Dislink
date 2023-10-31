from nextcord import Interaction
from nextcord.ext import commands
from nextcord.ext.commands import Context

class ErrorHandlingCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error: BaseException):
        # Игнорировать ошибку, если она была успешно обработана внутри команды
        if hasattr(ctx.command, 'on_error'):
            return

        # Игнорировать ошибку, если команда запрещена для выполнения
        if isinstance(error, commands.DisabledCommand):
            return

        # Обработка ошибки неправильных аргументов команды
        if isinstance(error, commands.BadArgument):
            await ctx.send(f'Неправильные аргументы команды. Пожалуйста, проверьте правильность ввода.')

        # Обработка ошибки, если не было указано обязательное аргументы
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'Не указан обязательный аргумент: {error.param.name}')

        # Обработка ошибки, если команда вызывается вне сервера
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send('Эту команду нельзя использовать в личных сообщениях.')

        # Обработка остальных ошибок
        else:
            await ctx.send(f'Произошла ошибка: {str(error)}')
    
    #@commands.Cog.listener()
    #async def on_slash_command_error(self, interaction: Interaction, error: BaseException):
    #    await interaction.send(f"error: {error}")
    # not allowed in nextcord, only in discord.py

def setup(bot):
    print("ErrorHandlingCog loaded!")
    bot.add_cog(ErrorHandlingCog(bot))
