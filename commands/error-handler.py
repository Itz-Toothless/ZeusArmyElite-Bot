import discord
from discord.ext import commands


class ErrorHandler(commands.Cog):
    def __init__(self , zeus):
        self.zeus = zeus

    @commands.Cog.listener()
    async def on_command_error(self , ctx: commands.Context , error: commands.CommandError):
        if isinstance(error , commands.CommandNotFound):
            print(f"[CommandNotFound] {ctx.author} - {ctx.author.id} hat einen Fehler erwischt: {error}")
            return await ctx.reply(f"{ctx.author.name} ein Fehler ist aufgetreten! {error}", mention_author = True)
        else:
            raise error


def setup(zeus):
    zeus.add_cog(ErrorHandler(zeus))
