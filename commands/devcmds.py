import asyncio
import contextlib
import datetime
import io
import os
import subprocess
from datetime import datetime

import discord
from discord.ext import commands


class dev(commands.Cog):
    def __init__(self , zeus):
        self.zeus = zeus

    @commands.command(aliases = ["exec"])
    @commands.is_owner()
    async def run(self , ctx , * , input_user):
        byte_data = subprocess.check_output([input_user] , shell = True)
        system_output = byte_data.decode('utf-8')
        embed = discord.Embed(timestamp = ctx.message.created_at, color = 0xff2200 , title = "Execution" ,
                              description = f"📥**Input:**```bash\n{input_user}\n```\n\n📤**Output:**```cos\n{system_output}\n```")
        embed.set_author(name = f"{ctx.author}" , icon_url = f"{ctx.author.avatar.url}")
        embed.set_footer(text = f"User-ID: {ctx.author.id}" , icon_url = ctx.author.avatar.url)
        return await ctx.reply(embed = embed , mention_author = False)

    @run.error
    async def runcmd_error(self , ctx , error):
        if isinstance(error , SyntaxError):
            return await ctx.send(f"{error}")
            print(f"{error}")
        elif isinstance(error , commands.CheckFailure):
            pass
        else:
            raise error

    @commands.command(aliases = ['execute'])
    @commands.is_owner()
    async def eval(self , ctx , * , code):
        str_obj = io.StringIO()
        try:
            with contextlib.redirect_stdout(str_obj):
                exec(code)
        except Exception as e:
            first_embed = discord.Embed(timestamp = ctx.message.created_at, title = "Auswertung..." ,
                                        description = f"**Wird ausgewertet:** \n```python\n{code}\n```..." ,
                                        color = 0xff0000)
            first_embed.set_author(name = f"{ctx.author}" , icon_url = ctx.author.avatar.url)
            first_embed.set_footer(text = f"User-ID: {ctx.author.id}" , icon_url = ctx.author.avatar.url)
            second_embed = discord.Embed(
                description = f"📥 **Eingabe:**\n\n```python\n{code}\n```\n\n📤 **Ausgabe:**\n\n```python\n{e.__class__.__name__}: {e}\n```" ,
                timestamp = ctx.message.created_at , title = "Ein Fehler wurde ausgegeben!" , color = 0xff2200)
            second_embed.set_author(name = f"{ctx.author}" , icon_url = ctx.author.avatar.url)
            second_embed.set_footer(text = f"User-ID: {ctx.author.id}" , icon_url = ctx.author.avatar.url)
            message = await ctx.reply(embed = first_embed , mention_author = False)
            await asyncio.sleep(3)
            await message.edit(embed = second_embed)
        else:
            first_embed = discord.Embed(timestamp = ctx.message.created_at, title = "Auswertung..." ,
                                        description = f"**Wird ausgewertet:** \n```python\n{code}\n```..." ,
                                        color = 0xff0000)
            first_embed.set_author(name = f"{ctx.author}" , icon_url = ctx.author.avatar.url)
            first_embed.set_footer(text = f"User-ID: {ctx.author.id}" , icon_url = ctx.author.avatar.url)
            second_embed = discord.Embed(
                description = f"📥 **Eingabe:**\n\n```python\n{code}\n```\n\n📤 **Ausgabe:**\n\n```python\n{str_obj.getvalue()}\n```" ,
                timestamp = ctx.message.created_at , title = "Auswertung abgeschlossen!" , color = 0x22ff00)
            second_embed.set_author(name = f"{ctx.author}" , icon_url = ctx.author.avatar.url)
            second_embed.set_footer(text = f"User-ID: {ctx.author.id}" , icon_url = ctx.author.avatar.url)
            message = await ctx.reply(embed = first_embed , mention_author = False)
            await asyncio.sleep(3)
            await message.edit(embed = second_embed)

    @eval.error
    async def eval_error(self , error):
        if isinstance(error , commands.CheckFailure):
            pass
        elif isinstance(error , commands.NotOwner):
            pass
        else:
            raise error

    @commands.command(aliases = ['s' , 'botsay'])
    @commands.is_owner()
    async def say(self , ctx , * , args):
        await ctx.send(args)
        await ctx.message.delete()

    @say.error
    async def say_error(self , error):
        if isinstance(error , commands.CheckFailure):
            pass
        elif isinstance(error , commands.NotOwner):
            pass
        else:
            raise error

    @commands.command(aliases = ["reload" , "update"])
    @commands.is_owner()
    async def load(self , ctx):
        await ctx.message.delete()
        for filename in os.listdir('./zeus'):
            if filename.endswith('.py'):
                try:
                    self.zeus.reload_extension(f'zeus.{filename[:-3]}')
                    await ctx.send(f"{filename} wurde neu geladen!" , delete_after = 1)
                    print(f"{filename} wurde neu geladen!")
                except Exception:
                    print(f"Fehler aufgetreten beim Laden von {filename}" , file = sys.stderr)
                    traceback.print_exc()

    @load.error
    async def load_error(self , error):
        if isinstance(error , commands.CheckFailure):
            pass
        elif isinstance(error , commands.NotOwner):
            pass
        else:
            raise error


def setup(zeus):
    zeus.add_cog(dev(zeus))
