import platform
import time
import discord
import psutil
import asyncio
from discord.ext import commands
from datetime import timedelta

startTime = time.time()


class botinfos(commands.Cog):
    def __init__(self , zeus):
        self.zeus = zeus

    @commands.command(aliases = ['bot-info' , 'boti', 'bot info'])
    @commands.guild_only()
    async def about(self , ctx):
        async with ctx.typing():
            await asyncio.sleep(0)
        em = discord.Embed(timestamp = ctx.message.created_at, title = f"{self.zeus.user}'s Information", color = 0xff2200)
        em.set_author(name = f"{ctx.author}", icon_url = f"{ctx.author.avatar.url}")
        em.add_field(name = "CPU Nutzung <:cpu:897289978105704458>:", value = f"{psutil.cpu_percent(4)}%", inline = True)
        em.add_field(name = "RAM Nutzung <:RAM:897289940411502592>:", value = f"{psutil.virtual_memory()[2]}%", inline = True)
        em.add_field(name = "Python Version <:python:897290376333885491>:", value = f"{platform.python_version()}", inline = True)
        em.add_field(name = "Bot Version ⚒️:" , value = f'Alpha 0.0.1' , inline = True)
        em.add_field(name = "Ping 🏓:" , value = f"{round(self.zeus.latency * 1000)}ms", inline=True)
        em.add_field(name = "Andere Informationen <:info:897290082959118406>:" , value = f'Kernel: {platform.system()} ' f' {platform.release()} \n', inline = True)
        em.add_field(name = "Uptime ⏲:" , value = f"{str(timedelta(seconds = int(round(time.time() - startTime))))}", inline = True)
        em.add_field(name = "Bot ID <:info:897290082959118406>:", value = f"{self.zeus.user.id}", inline = True)
        em.add_field(name="Invite 📬:", value = f"[Admin Invite](https://discord.com/api/oauth2/authorize?client_id=901585159848095765&permissions=8&scope=bot)\n[Invite](https://discord.com/api/oauth2/authorize?client_id=901585159848095765&permissions=395673173238&scope=bot)")
        em.set_thumbnail(url = f"{self.zeus.user.avatar.url}")
        em.set_footer(text = f"User-ID: {ctx.author.id}" , icon_url = f"{ctx.author.avatar.url}")
        return await ctx.reply(embed = em , mention_author = False)

    @commands.command(aliases = ['p', 'latency', 'bot-latency'])
    @commands.guild_only()
    async def ping(self , ctx):
        message = await ctx.send(f"**Ping :satellite:**...")
        await asyncio.sleep(1)
        await message.edit(content = f'**Pong 🏓: {round(self.zeus.latency * 1000)}ms**')


def setup(zeus):
    zeus.add_cog(botinfos(zeus))
