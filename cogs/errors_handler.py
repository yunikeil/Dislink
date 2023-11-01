from nextcord import Interaction
from nextcord.ext import commands
from nextcord.ext.commands import Context

# TODO попробовать переписать на discord.py с нуля все коги
class ErrorHandlingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_error(self, error):
        print(type(error), error)

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error: BaseException):
        await ctx.send(error)
    
    
    @commands.Cog.listener()
    async def on_application_command_error(self, interaction: Interaction, error: BaseException):
        await interaction.send(error)
    

def setup(bot):
    print("ErrorHandlingCog loaded!")
    bot.add_cog(ErrorHandlingCog(bot))
