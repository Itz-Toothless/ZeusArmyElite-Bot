import datetime
from datetime import datetime
from typing import Union
import discord
from discord.ext import commands


class infos(commands.Cog):
    def __init__(self , zeus):
        self.zeus = zeus

    @commands.command(aliases = ["serveri" , "server-info" , "si" , "server info"])
    async def serverinfo(self , ctx):
        server_name = str(ctx.guild.name)
        server_owner = str(ctx.guild.owner)
        verification_lvl = str(ctx.guild.verification_level)
        description = str(ctx.guild.description)
        id = str(ctx.guild.id)
        region = str(ctx.guild.region)
        text_ch = str(len(ctx.guild.text_channels))
        voice_ch = str(len(ctx.guild.voice_channels))
        icon = str(ctx.guild.icon.url)
        role_count = len(ctx.guild.roles - 1)
        rules = None if not ctx.guild.rules_channel else str(ctx.guild.rules_channel.name)
        roles = ', '.join([str(r.mention) for r in ctx.guild.roles[:0:-1]])
        d1 = ctx.guild.created_at
        level = verification_lvl.capitalize()
        region = region.capitalize()

        embed = discord.Embed(timestamp = ctx.message.created_at , color = discord.Colour.random() ,
                              title = "Server-Info")
        embed.set_author(name = f"{ctx.author}" , icon_url = f"{ctx.author.avatar.url}")
        embed.add_field(name = "Server-Name" , value = f"{server_name}" , inline = False)
        embed.add_field(name = "Server erstellt am:" , value = "<t:{}:{}>".format(int(d1.timestamp()) , 'F') ,
                        inline = False)
        embed.add_field(name = "Server-Owner" , value = f"{server_owner}" , inline = False)
        embed.add_field(name = "Server-ID" , value = f"{id}" , inline = False)
        embed.add_field(name = "Server-Beschreibung" , value = f"{description}" , inline = False)
        embed.add_field(name = "Verifikations-Level" , value = f"{level}" , inline = False)
        embed.add_field(name = "Region" , value = f"{region}" , inline = False)
        embed.add_field(name = "Regeln-Kanal", value = f"{rules}", inline = False)
        embed.add_field(name = "Server-Textkanäle" , value = f"{text_ch}" , inline = False)
        embed.add_field(name = "Server-Sprachkanäle" , value = f"{voice_ch}" , inline = False)
        embed.add_field(name = f"Rollen [{role_count}]" , value = f"{roles}" , inline = False)
        embed.set_thumbnail(url = icon)
        return await ctx.reply(embed = embed)

    @commands.command(aliases = ["user" , "user-info" , "user_info" , "uinfo" , "u-info" , "info", "minfo", "memberinfo", "member-info", "member_info"])
    async def userinfo(self , ctx , * , user: Union[discord.Member, discord.User] = None):
        if user is None:
            voice_state = "Keine Sprach-Kanal Aktivität erkannt" if not ctx.author.voice else ctx.author.voice.channel
            d1 = ctx.author.created_at
            d2 = ctx.author.joined_at
            presence = str(ctx.author.status).capitalize()
            timestamp = ctx.message.created_at
            server_timestamp = "**<t:{}:{}>**".format(int(d2.timestamp()) , "F")
            embed_color = 0xff2200
            discord_timestamp = "**<t:{}:{}>**".format(int(d1.timestamp()) , "F")
            roles = "Keine Rollen erkannt" if not ctx.author.roles[:0:-1] else ', '.join(
                r.mention for r in ctx.author.roles[:0:-1])
            url = ctx.author.avatar.url
            embed = discord.Embed(timestamp = timestamp , color = embed_color ,
                                  title = f"Informationen über " + str(ctx.author))
            embed.set_author(name = str(ctx.author) , icon_url = url)
            embed.set_thumbnail(url = url)
            embed.add_field(name = ":credit_card: Discord beigetreten am:" ,
                            value = discord_timestamp , inline = True)
            embed.add_field(name = ":credit_card: Server beigetreten am:" ,
                            value = server_timestamp , inline = True)
            embed.add_field(name = 'Nick' , value = ctx.author.nick , inline = True)
            embed.add_field(name = 'Präsenz' , value = presence , inline = True)
            embed.add_field(name = 'Sprachkanal Aktivität' , value = voice_state , inline = True)
            if ctx.author.guild_permissions.administrator:
                embed.add_field(name = "Admin?" , value = "<:Ja_Yes:896789260248686695>" , inline = True)
            else:
                embed.add_field(name = "Admin?" , value = "<:No:896789214581117020>" , inline = True)
            if ctx.author.bot:
                embed.add_field(name = "Bot?" , value = "<:Ja_Yes:896789260248686695>" , inline = True)
            else:
                embed.add_field(name = "Bot?" , value = "<:No:896789214581117020>" , inline = True)
            embed.add_field(name = "Rollen: [{}]".format(len(ctx.author.roles) - 1) , value = roles , inline = False)
            perm_string = ', '.join(
                [str(p[0]).replace("_" , " ").title() for p in ctx.author.guild_permissions if p[1]])
            embed.add_field(name = "<:Cmd:896789400250363934> Server Berechtigungen:" , value = perm_string ,
                            inline = False)
            embed.set_footer(text = '💳 ID: ' + str(ctx.author.id))
            return await ctx.send(embed = embed)
        elif isinstance(user, discord.Member):  # if a user has been specified and if it's an member of the server
            voice_state = "Keine Sprach-Kanal Aktivität erkannt" if not user.voice else user.voice.channel
            d1 = user.created_at
            d2 = user.joined_at
            presence = str(user.status).capitalize()
            timestamp = ctx.message.created_at
            server_timestamp = "**<t:{}:{}>**".format(int(d2.timestamp()) , "F")
            embed_color = 0xff2200
            discord_timestamp = "**<t:{}:{}>**".format(int(d1.timestamp()) , "F")
            roles = "Keine Rollen erkannt" if not user.roles[:0:-1] else ', '.join([r.mention for r in user.roles[:0:-1]])
            url = user.avatar.url
            embed = discord.Embed(timestamp = timestamp , color = embed_color ,
                                  title = f"Informationen über " + str(user) ,
                                  description = f"{user.mention}")
            embed.set_author(name = str(user) , icon_url = url)
            embed.set_thumbnail(url = url)
            embed.add_field(name = ":credit_card: Discord beigetreten am:" ,
                            value = discord_timestamp , inline = True)
            embed.add_field(name = ":credit_card: Server beigetreten am:",
                            value = server_timestamp , inline = True)
            embed.add_field(name = 'Nick' , value = user.nick , inline = True)
            embed.add_field(name = 'Präsenz' , value = presence , inline = True)
            embed.add_field(name = 'Sprachkanal Aktivität' , value = voice_state , inline = True)
            if user.guild_permissions.administrator:
                embed.add_field(name = "Admin?" , value = "<:Ja_Yes:896789260248686695>" , inline = True)
            else:
                embed.add_field(name = "Admin?" , value = "<:No:896789214581117020>" , inline = True)
            if user.bot:
                embed.add_field(name = "Bot?" , value = "<:Ja_Yes:896789260248686695>" , inline = True)
            else:
                embed.add_field(name = "Bot?" , value = "<:No:896789214581117020>" , inline = True)
            embed.add_field(name="Rollen: [{}]".format(len(user.roles) - 1), value = roles, inline = False)
            perm_string = ', '.join([str(p[0]).replace("_" , " ").title() for p in user.guild_permissions if p[1]])
            embed.add_field(name = "<:Cmd:896789400250363934> Server Berechtigungen:" , value = perm_string ,
                            inline = False)
            embed.set_footer(text = '💳 ID: ' + str(user.id))
            return await ctx.send(embed = embed)
        elif isinstance(user, discord.User):  # if a user has been specified which isn't in the guild
            d1 = user.created_at
            embed = discord.Embed(timestamp = ctx.message.created_at , color = 0xff2200 ,
                                  title = f"Informationen über {user}",
                                  description = f"{user.mention}")
            embed.set_author(name = f"{user}" , icon_url = user.avatar.url)
            embed.set_thumbnail(url = user.avatar.url)
            embed.add_field(name = ":credit_card: Discord beigetreten am:" ,
                            value = "**<t:{}:{}>**".format(int(d1.timestamp()) , "F") , inline = False)
            if user.bot:
                embed.add_field(name = "Bot?" , value = "<:Ja_Yes:896789260248686695>" , inline = False)
            else:
                embed.add_field(name = "Bot?" , value = "<:No:896789214581117020>" , inline = False)
            embed.add_field(name = "💳 ID: " , value = f"**{user.id}**" , inline = False)
            embed.set_footer(text = f"User-ID: {ctx.author.id}")
            return await ctx.send(embed = embed)
        else:
            voice_state = "Keine Sprach-Kanal Aktivität erkannt" if not ctx.author.voice else ctx.author.voice.channel
            d1 = ctx.author.created_at
            d2 = ctx.author.joined_at
            presence = str(ctx.author.status).capitalize()
            timestamp = ctx.message.created_at
            server_timestamp = "**<t:{}:{}>**".format(int(d2.timestamp()) , "F")
            embed_color = 0xff2200
            discord_timestamp = "**<t:{}:{}>**".format(int(d1.timestamp()) , "F")
            roles = "Keine Rollen erkannt" if not ctx.author.roles[:0:-1] else ', '.join(r.mention for r in ctx.author.roles[:0:-1])
            url = ctx.author.avatar.url
            embed = discord.Embed(timestamp = timestamp , color = embed_color ,
                                  title = f"Informationen über " + str(ctx.author))
            embed.set_author(name = str(ctx.author) , icon_url = url)
            embed.set_thumbnail(url = url)
            embed.add_field(name = ":credit_card: Discord beigetreten am:" ,
                            value = discord_timestamp , inline = True)
            embed.add_field(name = ":credit_card: Server beigetreten am:" ,
                            value = server_timestamp , inline = True)
            embed.add_field(name = 'Nick' , value = ctx.author.nick , inline = True)
            embed.add_field(name = 'Präsenz' , value = presence , inline = True)
            embed.add_field(name = 'Sprachkanal Aktivität' , value = voice_state , inline = True)
            if ctx.author.guild_permissions.administrator:
                embed.add_field(name = "Admin?" , value = "<:Ja_Yes:896789260248686695>" , inline = True)
            else:
                embed.add_field(name = "Admin?" , value = "<:No:896789214581117020>" , inline = True)
            if ctx.author.bot:
                embed.add_field(name = "Bot?" , value = "<:Ja_Yes:896789260248686695>" , inline = True)
            else:
                embed.add_field(name = "Bot?" , value = "<:No:896789214581117020>" , inline = True)
            embed.add_field(name = "Rollen: [{}]".format(len(ctx.author.roles) - 1) , value = roles , inline = False)
            perm_string = ', '.join([str(p[0]).replace("_" , " ").title() for p in ctx.author.guild_permissions if p[1]])
            embed.add_field(name = "<:Cmd:896789400250363934> Server Berechtigungen:" , value = perm_string ,
                            inline = False)
            embed.set_footer(text = '💳 ID: ' + str(ctx.author.id))
            return await ctx.send(embed = embed)

    @userinfo.error  # If the member couldn't be found
    async def info_error(self , ctx , error):
        if isinstance(error , commands.MemberNotFound):
            voice_state = "Keine Sprach-Kanal Aktivität erkannt" if not ctx.author.voice else ctx.author.voice.channel
            d1 = ctx.author.created_at
            d2 = ctx.author.joined_at
            presence = str(ctx.author.status).capitalize()
            timestamp = ctx.message.created_at
            server_timestamp = "**<t:{}:{}>**".format(int(d2.timestamp()) , "F")
            embed_color = 0xff2200
            discord_timestamp = "**<t:{}:{}>**".format(int(d1.timestamp()) , "F")
            roles = "Keine Rollen erkannt" if not ctx.author.roles[:0:-1] else ', '.join(
                r.mention for r in ctx.author.roles[:0:-1])
            url = ctx.author.avatar.url
            embed = discord.Embed(timestamp = timestamp , color = embed_color ,
                                  title = f"Informationen über " + str(ctx.author))
            embed.set_author(name = str(ctx.author) , icon_url = url)
            embed.set_thumbnail(url = url)
            embed.add_field(name = ":credit_card: Discord beigetreten am:" ,
                            value = discord_timestamp , inline = True)
            embed.add_field(name = ":credit_card: Server beigetreten am:" ,
                            value = server_timestamp , inline = True)
            embed.add_field(name = 'Nick' , value = ctx.author.nick , inline = True)
            embed.add_field(name = 'Präsenz' , value = presence , inline = True)
            embed.add_field(name = 'Sprachkanal Aktivität' , value = voice_state , inline = True)
            if ctx.author.guild_permissions.administrator:
                embed.add_field(name = "Admin?" , value = "<:Ja_Yes:896789260248686695>" , inline = True)
            else:
                embed.add_field(name = "Admin?" , value = "<:No:896789214581117020>" , inline = True)
            if ctx.author.bot:
                embed.add_field(name = "Bot?" , value = "<:Ja_Yes:896789260248686695>" , inline = True)
            else:
                embed.add_field(name = "Bot?" , value = "<:No:896789214581117020>" , inline = True)
            embed.add_field(name = "Rollen: [{}]".format(len(ctx.author.roles) - 1) , value = roles , inline = False)
            perm_string = ', '.join(
                [str(p[0]).replace("_" , " ").title() for p in ctx.author.guild_permissions if p[1]])
            embed.add_field(name = "<:Cmd:896789400250363934> Server Berechtigungen:" , value = perm_string ,
                            inline = False)
            embed.set_footer(text = '💳 ID: ' + str(ctx.author.id))
            return await ctx.send(embed = embed)
        elif isinstance(error , commands.UserNotFound):
            voice_state = "Keine Sprach-Kanal Aktivität erkannt" if not ctx.author.voice else ctx.author.voice.channel
            d1 = ctx.author.created_at
            d2 = ctx.author.joined_at
            presence = str(ctx.author.status).capitalize()
            timestamp = ctx.message.created_at
            server_timestamp = "**<t:{}:{}>**".format(int(d2.timestamp()) , "F")
            embed_color = 0xff2200
            discord_timestamp = "**<t:{}:{}>**".format(int(d1.timestamp()) , "F")
            roles = "Keine Rollen erkannt" if not ctx.author.roles[:0:-1] else ', '.join(
                r.mention for r in ctx.author.roles[:0:-1])
            url = ctx.author.avatar.url
            embed = discord.Embed(timestamp = timestamp , color = embed_color ,
                                  title = f"Informationen über " + str(ctx.author))
            embed.set_author(name = str(ctx.author) , icon_url = url)
            embed.set_thumbnail(url = url)
            embed.add_field(name = ":credit_card: Discord beigetreten am:" ,
                            value = discord_timestamp , inline = True)
            embed.add_field(name = ":credit_card: Server beigetreten am:" ,
                            value = server_timestamp , inline = True)
            embed.add_field(name = 'Nick' , value = ctx.author.nick , inline = True)
            embed.add_field(name = 'Präsenz' , value = presence , inline = True)
            embed.add_field(name = 'Sprachkanal Aktivität' , value = voice_state , inline = True)
            if ctx.author.guild_permissions.administrator:
                embed.add_field(name = "Admin?" , value = "<:Ja_Yes:896789260248686695>" , inline = True)
            else:
                embed.add_field(name = "Admin?" , value = "<:No:896789214581117020>" , inline = True)
            if ctx.author.bot:
                embed.add_field(name = "Bot?" , value = "<:Ja_Yes:896789260248686695>" , inline = True)
            else:
                embed.add_field(name = "Bot?" , value = "<:No:896789214581117020>" , inline = True)
            embed.add_field(name = "Rollen: [{}]".format(len(ctx.author.roles) - 1) , value = roles , inline = False)
            perm_string = ', '.join(
                [str(p[0]).replace("_" , " ").title() for p in ctx.author.guild_permissions if p[1]])
            embed.add_field(name = "<:Cmd:896789400250363934> Server Berechtigungen:" , value = perm_string ,
                            inline = False)
            embed.set_footer(text = '💳 ID: ' + str(ctx.author.id))
            return await ctx.send(embed = embed)
        else:
            raise error

    @commands.command(aliases=["perm_string", "perms", "permissions"])
    async def allperms(self, ctx):
        embed = discord.Embed(timestamp = ctx.message.created_at, color = 0xff2200,
                              title = "Alle Berechtigungen",
                              description="**Text-Kanäle Berechtigungen:**\nCreate Instant Invite: Einladung erstellen\nAdd Reactions: Reaktionen hinzufügen\nRead Messages: Nachrichten Lesen\nSend Messages: Nachrichten Senden\nEmbed Links: Links einbetten\nAttach Files: Dateien anhängen\nRead Message History: Nachrichtenverlauf anschauen\nMention Everyone: @here und @everyone erwähnen\nExternal Emojis: Externe Emojis verwenden\nUse Slash Commands: Anwendungsbefehle verwenden\nExternal Stickers: Externe Sticker verwenden\n\n**Mitglieder Berechtigungen:**\n\n\n\n**Thread-Kanäle Berechtigungen:**\nCreate Public Threads: Öffentliche Threads eröffnen\nCreate Private Threads: Private Threads eröffnen\nManage Threads: Threads verwalten\nSend Messages in Threads: Nachrichten in Threads versenden\n\n**Sprach-Kanäle Berechtigungen:**\nConnect: Verbinden\nSpeak: Sprechen\nUse Voice Activation (short: UVA): Sprachaktivierung verwenden\nStream: Streamen\n\n**Stage-Kanäle Berechtigungen:**\nVery Important Speaker: Sehr wichtiger Sprecher\nRequest to Speak: Redeanfrage versenden")
        embed.set_author(name=f"{ctx.author}", icon_url = f"{ctx.author.avatar.url}")
        embed.set_footer(text=f"User-ID: {ctx.author.id}", icon_url = f"{ctx.author.avatar.url}")
        return await ctx.reply(embed=embed, mention_author = False)

    @commands.command(aliases=["role-info", "rinfo", "role-whois", "r-whois"])
    async def roleinfo(self, ctx, role: discord.Role = None):
        role_color = role.color
        role_date = role.created_at
        role_mention = role.mention
        role_hoist = "<:No:896789214581117020>" if not role.hoist else "<:Yes:902117760195252266>"
        role_mentionable = "<:No:896789214581117020>" if not role.mentionable else "<:Yes:902117760195252266>"
        role_botmanaged = "<:No:896789214581117020>" if not role.is_bot_managed() else "<:Yes:902117760195252266>"
        role_name = role.name
        role_id = role.id
        role_permissions = ', '.join(
                    [str(p[0]).replace("_" , " ").title() for p in role.permissions if p[1]])

        embed = discord.Embed(timestamp = ctx.message.created_at, color = role_color, title = f"Rollen-Info")
        embed.add_field(name="Rolle erstellt am:", value="**<t:{}:{}>**".format(int(role_date.timestamp()), "F"), inline = False)
        embed.add_field(name="Rollen Ping:", value=f"{role_mention}", inline = False)
        embed.add_field(name="Rollen Name:", value = f"{role_name}", inline = False)
        embed.add_field(name="Rollen ID:", value = f"{role_id}", inline = False)
        embed.add_field(name="Gruppiert?:", value=f"{role_hoist}", inline = False)
        embed.add_field(name="Pingbar für andere Nutzer?:", value=f"{role_mentionable}", inline = False)
        embed.add_field(name="Verwaltet von einem Bot?:", value = f"{role_botmanaged}", inline = False)
        embed.add_field(name="Rollen Berechtigungen", value = f"{role_permissions}", inline = False)
        return await ctx.reply(embed=embed, mention_author = True)

    @roleinfo.error
    async def role_not_found(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            return await ctx.reply("Bitte erwähne eine Rolle oder benutze eine Rollen-ID, um Infos über diese zu erhalten!")
        elif isinstance(error, commands.RoleNotFound):
            return await ctx.reply("Diese Rolle existiert auf diesem Server nicht!")

    @commands.command(aliases = ['q'])
    async def quote(self, ctx, message: discord.Message):
        url = message.jump_url
        content = message.content
        channel_name = message.channel.name
        created_at = message.created_at
        embed = discord.Embed(timestamp = ctx.message.created_at, color = message.author.colour , description = "{}".format(content))
        embed.set_author(name = str(message.author) , icon_url = message.author.avatar.url)
        embed.add_field(name = "Link" , value = '[Springe zur Nachricht]({})'.format(url) , inline = True)
        embed.add_field(name = "Geschrieben am:", value = "**<t:{}:{}>**".format(int(created_at.timestamp()), "F"), inline = True)
        embed.set_footer(text = "#{}".format(channel_name))
        return await ctx.reply(embed = embed)

    @quote.error
    async def quote_errors(self, ctx, error):
        if isinstance(error, commands.ChannelNotFound):
            return await ctx.reply(f"{ctx.author} der Kanal konnte nicht gefunden werden!")
        elif isinstance(error, commands.MessageNotFound):
            return await ctx.reply(f"{ctx.author} die Nachricht wurde nicht gefunden, womöglich existiert diese nicht mehr!")
        else:
            raise error


def setup(zeus):
    zeus.add_cog(infos(zeus))
