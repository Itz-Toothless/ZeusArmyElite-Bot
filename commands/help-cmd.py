import discord
from discord.ext import commands


class helpcmd(commands.Cog):
    def __init__(self , zeus):
        self.zeus = zeus

    @commands.group(aliases = ['h'] , invoke_without_command = True)
    @commands.guild_only()
    async def help(self , ctx):
        em = discord.Embed(timestamp = ctx.message.created_at , color = 0xff2200 , title = f"ZAE's Commands" ,
                           description = "**Moderation:**\nzae!help moderation (Alias: zae!help mod)\n\n**Information:**\nzae!help information (Alias: zae!help info)\n\n**Bot-Informations**\nzae!help botinfo (Alias: zae!help bot)")
        em.set_author(name = f"{ctx.author}" , icon_url = f"{ctx.author.avatar.url}")
        em.set_thumbnail(url = f"{self.zeus.user.avatar.url}")
        em.set_footer(text = f"User-ID: {ctx.author.id}" , icon_url = f"{ctx.author.avatar.url}")
        return await ctx.reply(embed = em , mention_author = False)

    @help.command(aliases = ['mod'])
    @commands.guild_only()
    async def moderation(self , ctx):
        embed = discord.Embed(timestamp = ctx.message.created_at , color = 0xff2200 ,
                              title = f"🛡Moderations-Commands🛡" ,
                              description = "**zae!ban** - Bannt ein Mitglied aus dem Server\n\n**zae!massban** - Bannt mehrere Personen\n\n**zae!massunban** - Entbannt mehrere Personen\n\n**zae!unban** - Entbannt einen Nutzer\n\n**zae!kick** - Kickt einen Nutzer\n\n**zae!lockdown** - Setzt einen Kanal für `@everyone` unter Quarantäne\n\n**zae!lockup** - Schaltet einen Kanal für `@everyone` frei\n\n**zae!mute** - Schaltet einen Nutzer stumm\n\n**zae!tempmute** - Schaltet einen Nutzer temporär stumm\n\n**zae!unmute** - Entstummt einen Nutzer\n\n**zae!massmute** - Stummt mehrere Mitglieder des Servers gleichzeitig\n\n**zae!massunmute** - Entstummt mehrere Mitglieder des Servers gleichzeitig\n\n**zae!clear** - Löscht eine bestimmte Anzahl von Nachrichten")
        embed.set_footer(text = f'User-ID: {ctx.author.id}' , icon_url = f"{ctx.author.avatar.url}")
        embed.set_author(name = f'{ctx.author}' , icon_url = f"{ctx.author.avatar.url}")
        embed.set_thumbnail(url = f"{self.zeus.user.avatar.url}")
        return await ctx.reply(embed = embed , mention_author = False)

    @help.command(aliases = ['info'])
    @commands.guild_only()
    async def information(self , ctx):
        embed = discord.Embed(timestamp = ctx.message.created_at , color = 0xff2200 ,
                              title = f"📜Informations-Commands📜" ,
                              description = "**zae!userinfo** - Zeigt Nutzer-Informationen\n\n**zae!serverinfo** - Zeigt Server-Informationen\n\n**zae!roleinfo** - Zeigt Rollen-Informationen\n\n**zae!channelinfo** - Zeigt Kanal-Informationen")
        embed.set_author(name = f'{ctx.author}' , icon_url = f'{ctx.author.avatar.url}')
        embed.set_footer(text = f'User-ID: {ctx.author.id}' , icon_url = f"{ctx.author.avatar.url}")
        embed.set_thumbnail(url = f"{self.zeus.user.avatar.url}")
        return await ctx.reply(embed = embed , mention_author = False)

    @help.command(aliases = ['dev'])
    @commands.guild_only()
    async def developer(self , ctx):
        embed = discord.Embed(timestamp = ctx.message.created_at , color = 0xff2200 ,
                              title = f'🛠Developer-Commands🛠' ,
                              description = "**zae!eval** - Python Code-Auswerter\n\n**zae!exec** - Command-Linien Auswertung (Typ: Linux Debian)\n\n**zae!say** - Nachrichten-Wiederholung")
        embed.set_author(name = f'{ctx.author}' , icon_url = f'{ctx.author.avatar.url}')
        embed.set_footer(text = f'User-ID: {ctx.author.id}' , icon_url = f"{ctx.author.avatar.url}")
        embed.set_thumbnail(url = f"{self.zeus.user.avatar.url}")
        return await ctx.reply(embed = embed , mention_author = False)

    @help.command(aliases = ["bot-info" , "botinfo", "bot"])
    @commands.guild_only()
    async def botinformation(self , ctx):
        embed = discord.Embed(timestamp = ctx.message.created_at , color = 0xff2200 ,
                              title = "📑Botinformations-Commands📑" ,
                              description = f"**zae!about** - Zeigt Informationen von {self.zeus.user}\n**zae!ping** - Zeigt die aktuelle Latenz")
        embed.set_footer(text = f"User-ID: {ctx.author.id}" , icon_url = f"{ctx.author.avatar.url}")
        embed.set_author(name = f"{ctx.author}" , icon_url = f"{ctx.author.avatar.url}")
        embed.set_thumbnail(url = f"{self.zeus.user.avatar.url}")
        return await ctx.reply(embed = embed , mention_author = False)


def setup(zeus):
    zeus.add_cog(helpcmd(zeus))
