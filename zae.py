import asyncio
import locale
import sys
import time
import traceback

import discord
from discord.ext import commands

intents = discord.Intents().all()

zeus = commands.Bot(commands.when_mentioned_or("<@901585159848095765>" , "<@!901585159848095765>" , "zae!" , 'ZAE!') ,
                    intents = intents)

zeus.remove_command("help")

startTime = time.time()

locale.setlocale(locale.LC_ALL , 'de_DE.UTF-8')


@zeus.event
async def statuschange():
    await zeus.wait_until_ready()
    while True:
        members = 0
        for guild in zeus.guilds:
            members += guild.member_count - 1

        await zeus.change_presence(activity = discord.Activity(type = discord.ActivityType.playing ,
                                                               name = f"mit zae!"))
        await asyncio.sleep(60)

        await zeus.change_presence(activity = discord.Activity(type = discord.ActivityType.watching ,
                                                               name = "die ZAE beim Wachsen zu"))
        await asyncio.sleep(60)

        await zeus.change_presence(
            activity = discord.Activity(type = discord.ActivityType.listening , name = "Musik mit Zeus"))
        await asyncio.sleep(60)

initial_extensions = [
    'zeus.mod',
    'zeus.infos',
    'zeus.devcmds',
    'zeus.botinfos',
    'zeus.logs'
]


@zeus.event
async def on_ready():
    print("--------------------------------------")
    for extension in initial_extensions:
        try:
            zeus.load_extension(extension)
            print(f"| Bereit: {extension}!✅")
        except Exception:
            print(f"| Fehler: {extension}!❌" , file = sys.stderr)
            traceback.print_exc()
    zeus.loop.create_task(statuschange())
    zeus.load_extension('jishaku')
    print(f"| Bereit: jishaku.py!✅")
    print("| Bereit: {0.user}!✅".format(zeus))
    print("--------------------------------------")


@zeus.group(aliases = ['h'] , invoke_without_command = True)
@commands.guild_only()
async def help(ctx):
    em = discord.Embed(timestamp = ctx.message.created_at , color = 0xff2200 , title = f"ZAE's Commands" ,
                       description = "**Moderation:**\nzae!help moderation (Alias: zae!help mod)\n\n**Information:**\nzae!help information (Alias: zae!help info)\n\n**Bot-Informations**\nzae!help botinfo (Alias: zae!help bot)")
    em.set_author(name = f"{ctx.author}" , icon_url = f"{ctx.author.avatar.url}")
    em.set_thumbnail(url = f"{zeus.user.avatar.url}")
    em.set_footer(text = f"User-ID: {ctx.author.id}" , icon_url = f"{ctx.author.avatar.url}")
    return await ctx.reply(embed = em , mention_author = False)


@help.command(aliases = ['mod'])
@commands.guild_only()
async def moderation(ctx):
    embed = discord.Embed(timestamp = ctx.message.created_at , color = 0xff2200 , title = f"🛡Moderations-Commands🛡" ,
                          description = "**zae!ban - Bannt ein Mitglied aus dem Server**\n\n**zae!banid - Bannt ein Nutzer aus dem Server**\n\n**zae!massban - Bannt mehrere Personen**\n\n**zae!massunban - Entbannt mehrere Personen**\n\n**zae!unban - Entbannt einen Nutzer**\n\n**zae!kick -Kickt einen Nutzer**\n\n**zae!lockdown - Setzt einen Kanal für `@everyone` unter Quarantäne**\n\n**zae!lockup - Schaltet einen Kanal für `@everyone` frei**\n\n**zae!mute - Schaltet einen Nutzer stumm**\n\n**zae!tempmute - Schaltet einen Nutzer temporär stumm**\n\n**zae!unmute - Entstummt einen Nutzer**\n\n**zae!clear - Löscht eine bestimmte Anzahl von Nachrichten**")
    embed.set_footer(text = f'User-ID: {ctx.author.id}' , icon_url = f"{ctx.author.avatar.url}")
    embed.set_author(name = f'{ctx.author}' , icon_url = f"{ctx.author.avatar.url}")
    embed.set_thumbnail(url = f"{zeus.user.avatar.url}")
    return await ctx.reply(embed = embed , mention_author = False)


@help.command(aliases = ['info'])
@commands.guild_only()
async def information(ctx):
    embed = discord.Embed(timestamp = ctx.message.created_at , color = 0xff2200 , title = f"📜Informations-Commands📜" ,
                          description = "**zae!userinfo - Zeigt Informationen über einen User, der nicht auf dem Server ist**\n\n**zae!memberinfo - Zeigt Informationen über ein Server-Mitglied**\n\n**zae!serverinfo - Zeigt Server-Informationen**\n\n**zae!roleinfo - Zeigt Rollen-Informationen**")
    embed.set_author(name = f'{ctx.author}' , icon_url = f'{ctx.author.avatar.url}')
    embed.set_footer(text = f'User-ID: {ctx.author.id}' , icon_url = f"{ctx.author.avatar.url}")
    embed.set_thumbnail(url = f"{zeus.user.avatar.url}")
    return await ctx.reply(embed = embed , mention_author = False)


@help.command(aliases = ['dev'])
@commands.guild_only()
async def developer(ctx):
    embed = discord.Embed(timestamp = ctx.message.created_at , color = 0xff2200 , title = f'🛠Developer-Commands🛠' ,
                          description = "**zae!eval - Python Code-Auswerter**\n\n**zae!exec - Command-Linien Auswertung (Typ: Linux Debian)**\n\n**zae!say - Nachrichten-Wiederholung**")
    embed.set_author(name = f'{ctx.author}' , icon_url = f'{ctx.author.avatar.url}')
    embed.set_footer(text = f'User-ID: {ctx.author.id}' , icon_url = f"{ctx.author.avatar.url}")
    embed.set_thumbnail(url = f"{zeus.user.avatar.url}")
    return await ctx.reply(embed = embed , mention_author = False)


@help.command(aliases = ["bot-info" , "botinfo"])
@commands.guild_only()
async def botinformation(ctx):
    embed = discord.Embed(timestamp = ctx.message.created_at , color = 0xff2200 ,
                          title = "📑Botinformations-Commands📑" ,
                          description = f"**zae!about - Zeigt Informationen von {zeus.user}**\n**zae!ping - Zeigt die aktuelle Latenz**")
    embed.set_footer(text = f"User-ID: {ctx.author.id}" , icon_url = f"{ctx.author.avatar.url}")
    embed.set_author(name = f"{ctx.author}" , icon_url = f"{ctx.author.avatar.url}")
    embed.set_thumbnail(url = f"{zeus.user.avatar.url}")
    return await ctx.reply(embed = embed , mention_author = False)


zeus.run("OTAxNTg1MTU5ODQ4MDk1NzY1.YXSAnA.YssnLwNeARCiNTz3lNpq1G9gRkU" , reconnect = True)
