import datetime
import io
import aiohttp
import asyncio
from datetime import datetime
from typing import Union
import discord
from discord.ext import commands


class infos(commands.Cog):
    def __init__(self , zeus):
        self.zeus = zeus

    @commands.command(aliases = ["serveri" , "server-info" , "si" , "server info"])
    @commands.guild_only()
    async def serverinfo(self , ctx):
        online_counter = 0
        idle_counter = 0
        dnd_counter = 0
        offline_counter = 0
        server_name = str(ctx.guild.name)
        mfa = "<:Ja_Yes:896789260248686695>" if ctx.guild.mfa_level != 0 else "<:No:896789214581117020>"
        server_owner = ctx.guild.owner
        server_owner_id = ctx.guild.owner.id
        verification_lvl = "Kein Verifizierungslevel" if ctx.guild.verification_level == 'none' else "Niedriges Verifizierungslevel" if ctx.guild.verification_level == "low" else "Mittleres Verifizierungslevel" if ctx.guild.verification_level == "medium" else "Hohes Verifizierungslevel" if ctx.guild.verification_level.name == "high" else "Höchstes Verifizierungslevel"
        description = str(ctx.guild.description)
        id = str(ctx.guild.id)
        d1 = ctx.guild.created_at
        creation = "<t:{}:{}>".format(int(d1.timestamp()) , 'F')
        region = "Europa" if ctx.guild.region.name == 'europe' else "Brasilien" if ctx.guild.region.name == 'brazil' else "Hongkong" if ctx.guild.region.name == 'hongkong' else "Indien" if ctx.guild.region.name == 'india' else 'Japan' if ctx.guild.region.name == "japan" else 'Singapur' if ctx.guild.region.name == "singapore" else 'Südafrika' if ctx.guild.region.name == "southafrica" else 'Sydney' if ctx.guild.region.name else 'Nordamerika'
        text_ch = str(len(ctx.guild.text_channels))
        voice_ch = str(len(ctx.guild.voice_channels))
        member_count = str(len(ctx.guild.members))
        role_count = len(ctx.guild.roles)
        rules = None if not ctx.guild.rules_channel else str(ctx.guild.rules_channel.name)
        roles = ', '.join([str(r.mention) for r in ctx.guild.roles[:0:-1]])
        level = verification_lvl.capitalize()
        region = region.capitalize()
        for i in ctx.guild.members:
            if i.status == discord.Status.online:
                online_counter += 1
            if i.status == discord.Status.idle:
                idle_counter += 1
            if i.status == discord.Status.dnd:
                dnd_counter += 1
            if i.status == discord.Status.offline:
                offline_counter += 1
        try:
            embed = discord.Embed(timestamp = ctx.message.created_at , color = discord.Colour.random() ,
                                  title = "Server-Info",
                                  description = f"**Server-Name:**\n{server_name}\n\n**Server erstellt am:**\n{creation}\n\n**Server-Inhaber:**\n{server_owner} - {server_owner_id}\n\n**Server-ID:**\n{id}\n\n**Server-Beschreibung:**\n{description}\n\n**Mitglieder-Anzahl:**\n{member_count}\n\n**Status-Zähler:**\n🟢: [{online_counter}] / 🟡: [{idle_counter}] / 🔴: [{dnd_counter}] / ⚫: [{offline_counter}]\n\n**Verifikations-Level:**\n{verification_lvl}\n\n**Zwei-Faktor Aktiv?**\n{mfa}\n\n**Region:**\n{region}\n\n**Regeln-Kanal:**\n{rules}\n\n**Server-TextKanäle:**\n{text_ch}\n\n**Server-SprachKanäle:**\n{voice_ch}\n\n**Rollen [{role_count}]:**\n{roles}")
            embed.set_author(name = f"{ctx.author}" , icon_url = f"{ctx.author.display_avatar}")
            embed.set_thumbnail(url = ctx.guild.icon)
            return await ctx.reply(embed = embed)
        except discord.HTTPException:
            embed = discord.Embed(timestamp = ctx.message.created_at , color = discord.Colour.random() ,
                                  title = "Server-Info" ,
                                  description = f"**Server-Name:**\n{server_name}\n\n**Server erstellt am:**\n{creation}\n\n**Server-Inhaber:**\n{server_owner} - {server_owner_id}\n\n**Server-ID:**\n{id}\n\n**Server-Beschreibung:**\n{description}\n\n**Mitglieder-Anzahl:**\n{member_count}\n\n**Status-Zähler:**\n🟢: [{online_counter}] / 🟡: [{idle_counter}] / 🔴: [{dnd_counter}] / ⚫: [{offline_counter}]\n\n**Verifikations-Level:**\n{verification_lvl}\n\n**Zwei-Faktor Aktiv?**\n{mfa}\n\n**Region:**\n{region}\n\n**Regeln-Kanal:**\n{rules}\n\n**Server-TextKanäle:**\n{text_ch}\n\n**Server-SprachKanäle:**\n{voice_ch}\n\n**Rollen [{role_count}]:**\nZu viele Rollen, um diese anzuzeigen!")
            embed.set_author(name = f"{ctx.author}" , icon_url = f"{ctx.author.display_avatar}")
            embed.set_thumbnail(url = ctx.author.display_avatar)
            return await ctx.reply(embed = embed)

    @commands.command(aliases = ["m-uinfo" , "mass-user" , "mass-userinfo"])
    @commands.guild_only()
    async def massuserinfo(self , ctx , targets: commands.Greedy[discord.User]):
        for x in targets:
            try:
                d1 = x.created_at
                url = x.display_avatar
                embed = discord.Embed(timestamp = ctx.message.created_at , color = 0xff2200 ,
                                      title = f"Informationen über {x}" ,
                                      description = f"{x.mention}")
                embed.set_author(name = f"{x}" , icon_url = f"{url}")
                embed.set_thumbnail(url = f"{url}")
                embed.add_field(name = ":credit_card: Discord beigetreten am:" ,
                                value = "**<t:{}:{}>**".format(int(d1.timestamp()) , "F") , inline = False)
                if x.bot:
                    embed.add_field(name = "Bot?" , value = "<:Ja_Yes:896789260248686695>" , inline = True)
                else:
                    embed.add_field(name = "Bot?" , value = "<:No:896789214581117020>" , inline = True)
                    embed.add_field(name = "💳 ID: " , value = f"**{x.id}**" , inline = False)
                    embed.set_footer(text = f"Autor-ID: {ctx.author.id}")
                    await ctx.send(embed = embed)
            except Exception as e:
                print(e)
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
                url = ctx.author.display_avatar
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
                    embed.add_field(name = "Admin?" , value = "<:Ja_Yes:896789260248686695>" , inline = False)
                else:
                    embed.add_field(name = "Admin?" , value = "<:No:896789214581117020>" , inline = False)
                if ctx.author.bot:
                    embed.add_field(name = "Bot?" , value = "<:Ja_Yes:896789260248686695>" , inline = True)
                else:
                    embed.add_field(name = "Bot?" , value = "<:No:896789214581117020>" , inline = True)
                embed.add_field(name = "Rollen: [{}]".format(len(ctx.author.roles) - 1) , value = roles ,
                                inline = False)
                perm_string = ', '.join(
                    [str(p[0]).replace("_" , " ").title() for p in ctx.author.guild_permissions if p[1]])
                embed.add_field(name = "<:Cmd:896789400250363934> Server Berechtigungen:" , value = perm_string ,
                                inline = False)
                embed.set_footer(text = '💳 ID: ' + str(ctx.author.id))
                await ctx.send(embed = embed)


    @massuserinfo.error
    async def on_command_error(self , ctx , error):
        if isinstance(error , commands.BadUnionArgument):
            raise error
        else:
            raise error
    
    @commands.command(aliases = ["user" , "user-info" , "user_info" , "uinfo" , "u-info" , "info", "minfo", "memberinfo", "member-info", "member_info"])
    @commands.guild_only()
    async def userinfo(self , ctx , * , user: Union[discord.Member, discord.User] = None):
        if user is None:
            voice_state = "Keine Sprach-Kanal Aktivität erkannt" if not ctx.author.voice else ctx.author.voice.channel
            d1 = ctx.author.created_at
            d2 = ctx.author.joined_at
            timestamp = ctx.message.created_at
            server_timestamp = "**<t:{}:{}>**".format(int(d2.timestamp()) , "F")
            embed_color = 0xff2200
            status = "<:status_online:906562454413262888>" if ctx.author.status == 'online' else "<:status_idle:906562420976254976>" if ctx.author.status == 'idle' else "<:status_dnd:906562391129591888>" if ctx.author.status == 'dnd' else "<:status_offline:906562331461423144>" if ctx.author.status == 'offline' else '<:status_streaming:913394334387273759>' if ctx.author.status == "streaming" else "❓"
            discord_timestamp = "**<t:{}:{}>**".format(int(d1.timestamp()) , "F")
            roles = "Keine Rollen erkannt" if not ctx.author.roles[:0:-1] else ', '.join(
                r.mention for r in ctx.author.roles[:0:-1])
            try:
                url = ctx.author.avatar.url
            except AttributeError:
                url = self.zeus.user.avatar.url
            embed = discord.Embed(timestamp = timestamp , color = embed_color ,
                                  title = f"Informationen über " + str(ctx.author))
            embed.set_author(name = str(ctx.author) , icon_url = url)
            embed.set_thumbnail(url = url)
            embed.add_field(name = ":credit_card: Discord beigetreten am:" ,
                            value = discord_timestamp , inline = True)
            embed.add_field(name = ":credit_card: Server beigetreten am:" ,
                            value = server_timestamp , inline = True)
            embed.add_field(name = 'Nick' , value = ctx.author.nick , inline = True)
            embed.add_field(name = 'Präsenz' , value = status , inline = True)
            embed.add_field(name = 'Sprachkanal Aktivität' , value = voice_state , inline = True)
            if ctx.author.guild_permissions.administrator:
                embed.add_field(name = "Admin?" , value = "<:Ja_Yes:896789260248686695>" , inline = False)
            else:
                embed.add_field(name = "Admin?" , value = "<:No:896789214581117020>" , inline = False)
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
            try:
                url = user.avatar.url
            except AttributeError:
                url = self.zeus.user.avatar.url
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
                embed.add_field(name = "Admin?" , value = "<:Ja_Yes:896789260248686695>" , inline = False)
            else:
                embed.add_field(name = "Admin?" , value = "<:No:896789214581117020>" , inline = False)
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
            try:
                url = user.avatar.url
            except AttributeError:
                url = self.zeus.user.avatar.url
            embed = discord.Embed(timestamp = ctx.message.created_at , color = 0xff2200 ,
                                  title = f"Informationen über {user}",
                                  description = f"{user.mention}")
            embed.set_author(name = f"{user}" , icon_url = url)
            embed.set_thumbnail(url = url)
            embed.add_field(name = ":credit_card: Discord beigetreten am:" ,
                            value = "**<t:{}:{}>**".format(int(d1.timestamp()) , "F") , inline = False)
            if user.bot:
                embed.add_field(name = "Bot?" , value = "<:Ja_Yes:896789260248686695>" , inline = True)
            else:
                embed.add_field(name = "Bot?" , value = "<:No:896789214581117020>" , inline = True)
            embed.add_field(name = "💳 ID: " , value = f"**{user.id}**" , inline = False)
            embed.set_footer(text = f"Autor-ID: {ctx.author.id}")
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
            try:
                url = ctx.author.avatar.url
            except AttributeError:
                url = self.zeus.avatar.url
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
                embed.add_field(name = "Admin?" , value = "<:Ja_Yes:896789260248686695>" , inline = False)
            else:
                embed.add_field(name = "Admin?" , value = "<:No:896789214581117020>" , inline = False)
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
        if isinstance(error , commands.UserNotFound):
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
        elif isinstance(error, commands.BadUnionArgument):
            embed = discord.Embed(color = discord.Colour.random(), title = "Fehler!",
                                  description = "Bitte gebe einen Nutzer an!\n\nzae!userinfo <user / id>")
            embed.set_footer(text = f"User-ID: {ctx.author.id}", icon_url = f"{ctx.message.author.avatar.url}")
            embed.set_author(name = f"{ctx.author}", icon_url = f"{ctx.author.avatar.url}")
            return await ctx.send(embed=embed)
        else:
            raise error


    @commands.command(aliases=["perm_string", "perms", "permissions"])
    @commands.guild_only()
    async def allperms(self, ctx):
        embed = discord.Embed(timestamp = ctx.message.created_at, color = 0xff2200,
                              title = "Alle Berechtigungen",
                              description="**Text-Kanäle Berechtigungen:**\nCreate Instant Invite: Einladung erstellen\nAdd Reactions: Reaktionen hinzufügen\nRead Messages: Nachrichten Lesen\nSend Messages: Nachrichten Senden\nEmbed Links: Links einbetten\nAttach Files: Dateien anhängen\nRead Message History: Nachrichtenverlauf anschauen\nMention Everyone: @here und @everyone erwähnen\nExternal Emojis: Externe Emojis verwenden\nUse Slash Commands: Anwendungsbefehle verwenden\nExternal Stickers: Externe Sticker verwenden\n\n**Mitglieder Berechtigungen:**\n\n\n\n**Thread-Kanäle Berechtigungen:**\nCreate Public Threads: Öffentliche Threads eröffnen\nCreate Private Threads: Private Threads eröffnen\nManage Threads: Threads verwalten\nSend Messages in Threads: Nachrichten in Threads versenden\n\n**Sprach-Kanäle Berechtigungen:**\nConnect: Verbinden\nSpeak: Sprechen\nUse Voice Activation (short: UVA): Sprachaktivierung verwenden\nStream: Streamen\n\n**Stage-Kanäle Berechtigungen:**\nVery Important Speaker: Sehr wichtiger Sprecher\nRequest to Speak: Redeanfrage versenden")
        embed.set_author(name=f"{ctx.author}", icon_url = f"{ctx.author.avatar.url}")
        embed.set_footer(text=f"User-ID: {ctx.author.id}", icon_url = f"{ctx.author.avatar.url}")
        return await ctx.reply(embed=embed, mention_author = False)

    @commands.command(aliases=["role-info", "rinfo", "role-whois", "r-whois"])
    @commands.guild_only()
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
        embed.add_field(name="Rollen Hex-Code:", value = role_color, inline = False)
        embed.add_field(name="Gruppiert?:", value=f"{role_hoist}", inline = False)
        embed.add_field(name="Pingbar für andere Nutzer?:", value=f"{role_mentionable}", inline = False)
        embed.add_field(name="Verwaltet von einem Bot?:", value = f"{role_botmanaged}", inline = False)
        embed.add_field(name="Rollen Berechtigungen", value = f"{role_permissions}", inline = False)
        return await ctx.reply(embed=embed, mention_author = True)

    @roleinfo.error
    async def role_not_found(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            return await ctx.reply("Diese Rolle konnte nicht gefunden werden! Wahrscheinlich liegt es an bestimmten Berechtigungen!")
        elif isinstance(error, commands.RoleNotFound):
            return await ctx.reply("Diese Rolle existiert auf diesem Server nicht!")

    @commands.command(aliases=["channel", "channel-info", "c-info", "ci", "c_info", "c info", "channel info", "channel_info"])
    async def channelinfo(self, ctx, channel: Union[discord.TextChannel, discord.StageChannel, discord.VoiceChannel, discord.StoreChannel, discord.CategoryChannel] = None):
        if isinstance(channel, discord.TextChannel):
            channel_creationdate = channel.created_at
            channel_name = channel.name
            channel_id = channel.id
            channel_mention = channel.mention
            channel_overwrites = "Keine Rollen erkannt" if not channel.overwrites else ', '.join(
                r.name for r in channel.overwrites)
            channel_overwrite_count = len(channel.overwrites)
            channel_category = channel.category
            channel_nsfw = "<:Yes:902117760195252266>" if channel.nsfw else "<:No:896789214581117020>"
            channel_sync = "<:Yes:902117760195252266>" if channel.permissions_synced else "<:No:896789214581117020>"
            embed = discord.Embed(timestamp = ctx.message.created_at, color = discord.Colour.random(),
                                  title = "Channel-Info")
            embed.add_field(name="ID", value=channel_id, inline=True)
            embed.add_field(name="Name", value = channel_name, inline = True)
            embed.add_field(name="Erwähnung", value = f"`{channel_mention}`", inline = True)
            embed.add_field(name = "Kategorie", value = channel_category, inline = True)
            embed.add_field(name="NSFW?", value = channel_nsfw, inline = True)
            embed.add_field(name="Berechtigungen Syncronisiert?", value = channel_sync, inline = True)
            embed.add_field(name="Erstellung", value = "**<t:{}:{}>**".format(int(channel_creationdate.timestamp()), "F"), inline = True)
            embed.add_field(name="Rollen [{}]".format(channel_overwrite_count), value = channel_overwrites, inline = True)
            embed.set_author(name = ctx.author, icon_url = ctx.author.avatar.url)
            return await ctx.send(embed=embed)
        elif isinstance(channel, discord.VoiceChannel):
            channel_creationdate = channel.created_at
            channel_name = channel.name
            channel_id = channel.id
            channel_mention = channel.mention
            channel_category = channel.category
            embed = discord.Embed(timestamp = ctx.message.created_at , color = discord.Colour.random() ,
                                  title = "Channel-Info")
            embed.add_field(name = "ID" , value = channel_id , inline = True)
            embed.add_field(name = "Name" , value = channel_name , inline = True)
            embed.add_field(name = "Erwähnung" , value = f"`{channel_mention}`" , inline = True)
            embed.add_field(name = "Kategorie" , value = channel_category , inline = True)
            embed.add_field(name = "Erstellung" ,
                            value = "**<t:{}:{}>**".format(int(channel_creationdate.timestamp()) , "F") , inline = True)
            embed.set_author(name = ctx.author , icon_url = ctx.author.avatar.url)
            return await ctx.send(embed = embed)
        elif isinstance(channel, discord.StageChannel):
            channel_creationdate = channel.created_at
            channel_name = channel.name
            channel_id = channel.id
            channel_mention = channel.mention
            channel_overwrites = "Keine Rollen erkannt" if not channel.overwrites else ', '.join(
                r.name for r in channel.overwrites)
            channel_overwrite_count = len(channel.overwrites)
            channel_category = channel.category
            embed = discord.Embed(timestamp = ctx.message.created_at , color = discord.Colour.random() ,
                                  title = "Channel-Info")
            embed.add_field(name = "ID" , value = channel_id , inline = True)
            embed.add_field(name = "Name" , value = channel_name , inline = True)
            embed.add_field(name = "Erwähnung" , value = f"`{channel_mention}`" , inline = True)
            embed.add_field(name = "Kategorie" , value = channel_category , inline = True)
            embed.add_field(name = "Erstellung" ,
                            value = "**<t:{}:{}>**".format(int(channel_creationdate.timestamp()) , "F") , inline = True)
            embed.add_field(name = "Rollen [{}]".format(channel_overwrite_count) , value = channel_overwrites ,
                            inline = False)
            embed.set_author(name = ctx.author , icon_url = ctx.author.avatar.url)
            return await ctx.send(embed = embed)
        elif isinstance(channel, discord.StoreChannel):
            channel_creationdate = channel.created_at
            channel_name = channel.name
            channel_id = channel.id
            channel_mention = channel.mention
            channel_overwrites = "Keine Rollen erkannt" if not channel.overwrites else ', '.join(
                r.name for r in channel.overwrites)
            channel_overwrite_count = len(channel.overwrites)
            channel_category = channel.category
            channel_nsfw = "<:Yes:902117760195252266>" if channel.nsfw else "<:No:896789214581117020>"
            embed = discord.Embed(timestamp = ctx.message.created_at , color = discord.Colour.random() ,
                                  title = "Channel-Info")
            embed.add_field(name = "ID" , value = channel_id , inline = True)
            embed.add_field(name = "Name" , value = channel_name , inline = True)
            embed.add_field(name = "Erwähnung" , value = f"`{channel_mention}`" , inline = True)
            embed.add_field(name = "Kategorie" , value = channel_category , inline = True)
            embed.add_field(name = "NSFW?" , value = channel_nsfw , inline = True)
            embed.add_field(name = "Erstellung" ,
                            value = "**<t:{}:{}>**".format(int(channel_creationdate.timestamp()) , "F") , inline = True)
            embed.add_field(name = "Rollen [{}]".format(channel_overwrite_count) , value = channel_overwrites ,
                            inline = False)
            embed.set_author(name = ctx.author , icon_url = ctx.author.avatar.url)
            return await ctx.send(embed = embed)
        elif isinstance(channel, discord.CategoryChannel):
            channel_creationdate = channel.created_at
            channel_id = channel.id
            channel_mention = channel.mention
            channel_overwrites = "Keine Rollen erkannt" if not channel.overwrites else ', '.join(
                r.name for r in channel.overwrites)
            channel_overwrite_count = len(channel.overwrites)
            channel_category = channel.name
            channel_sync = "<:Yes:902117760195252266>" if channel.permissions_synced else "<:No:896789214581117020>"
            channel_nsfw = "<:Yes:902117760195252266>" if channel.nsfw else "<:No:896789214581117020>"
            embed = discord.Embed(timestamp = ctx.message.created_at , color = discord.Colour.random() ,
                                  title = "Channel-Info")
            embed.add_field(name = "ID" , value = channel_id , inline = True)
            embed.add_field(name = "Name" , value = channel_category , inline = True)
            embed.add_field(name = "Erwähnung" , value = f"`{channel_mention}`" , inline = True)
            embed.add_field(name = "NSFW?" , value = channel_nsfw , inline = True)
            embed.add_field(name = "Berechtigungen Syncronisiert?" , value = channel_sync , inline = True)
            embed.add_field(name = "Erstellung" ,
                            value = "**<t:{}:{}>**".format(int(channel_creationdate.timestamp()) , "F") , inline = True)
            embed.add_field(name = "Rollen [{}]".format(channel_overwrite_count) , value = channel_overwrites ,
                            inline = True)
            embed.set_author(name = ctx.author , icon_url = ctx.author.avatar.url)
            return await ctx.send(embed=embed)
        else:
            embed = discord.Embed(timestamp = ctx.message.created_at , color = discord.Colour.random(),
                                  title = "Fehler aufgetreten!" ,
                                  description = "Erwähne einen Kanal mit der ID oder einem Ping!\n\n**`zae!channelinfo (#channel / id)`**")
            embed.set_author(name = ctx.author , icon_url = ctx.author.avatar.url)
            embed.set_footer(text = "User-ID: {}".format(ctx.author.id) , icon_url = ctx.author.avatar.url)
            return await ctx.send(embed = embed)

    @channelinfo.error
    async def channel_not_found(self, ctx, error):
        if isinstance(error , commands.ChannelNotFound):
            embed = discord.Embed(timestamp = ctx.message.created_at , color = discord.Colour.random() ,
                                  title = "Fehler aufgetreten!" ,
                                  description = "Der Kanal konnte nicht gefunden werden!")
            embed.set_author(name = ctx.author , icon_url = ctx.author.avatar.url)
            embed.set_footer(text = "User-ID: {}".format(ctx.author.id) , icon_url = ctx.author.avatar.url)
            await asyncio.sleep(2)
            await ctx.message.delete()
            return await ctx.send(embed = embed , delete_after = 4)
        elif isinstance(error, commands.BadUnionArgument):
            embed = discord.Embed(timestamp = ctx.message.created_at , color = discord.Colour.random() ,
                                  title = "Fehler aufgetreten!" ,
                                  description = "Der Kanal konnte nicht gefunden werden!")
            embed.set_author(name = ctx.author , icon_url = ctx.author.avatar.url)
            embed.set_footer(text = "User-ID: {}".format(ctx.author.id) , icon_url = ctx.author.avatar.url)
            await asyncio.sleep(2)
            await ctx.message.delete()
            return await ctx.send(embed = embed , delete_after = 4)
        else:
            raise error

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
