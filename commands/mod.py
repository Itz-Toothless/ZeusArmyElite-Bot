import discord
from discord.ext import commands
import asyncio
from typing import Union
import time
import datetime
from datetime import timedelta , datetime


class mod(commands.Cog):
    def __init__(self , zeus):
        self.zeus = zeus

    @commands.command(name = "unban" , description = "Entbannt einen User mit seiner ID" ,
                      usage = "zae!unban <User-ID>")
    @commands.guild_only()
    @commands.has_guild_permissions(ban_members = True)
    @commands.bot_has_guild_permissions(ban_members = True)
    async def unban(self , ctx , user: discord.User = None , * , reason="Kein Grund angegeben"):
        if user is None:
            return await ctx.reply(f"{ctx.author.mention} erwähne eine Nutzer-ID!")
        else:
            await ctx.guild.unban(user , reason = reason)
            embed = discord.Embed(timestamp = ctx.message.created_at , color = discord.Color.random() ,
                                  title = "Entbannung ausgeführt" ,
                                  description = f"User: {user}\nModerator: {ctx.author}\nGrund: {reason}")
            embed.set_footer(text = f"User-ID: {ctx.author.id}" , icon_url = f"{ctx.message.author.display_avatar}")
            embed.set_author(name = f"{ctx.author}" , icon_url = f"{ctx.message.author.display_avatar}")
            return await ctx.reply(embed = embed , mention_author = True)

    @unban.error
    async def user_not_found(self , ctx , error):
        if isinstance(error , commands.UserNotFound):
            return await ctx.reply("Der Nutzer konnte nicht gefunden werden!")
        elif isinstance(error , commands.MissingPermissions):
            return await ctx.reply("Dir fehlt folgende Berechtigung: `BAN_MEMBERS`!")
        elif isinstance(error , commands.BotMissingPermissions):
            return await ctx.reply("Mir fehlt folgende Berechtigung: `BAN_MEMBERS`!")
        elif isinstance(error , commands.CommandInvokeError):
            return await ctx.reply("Der Nutzer ist nicht gebannt!")
        else:
            raise error

    @commands.command(name = "ban" , description = "Verbannt einen Nutzer vom Server" ,
                      usage = "zae!ban <User-ID/@ping> [Grund]")
    @commands.guild_only()
    @commands.has_permissions(ban_members = True)
    @commands.bot_has_permissions(ban_members = True)
    async def ban(self , ctx , user: Union[discord.Member , discord.User] = None , * , reason="Kein Grund angegeben"):
        if user is None:
            em = discord.Embed(timestamp = ctx.message.created_at , color = 0xff2200 , title = "Argumente Fehlen" ,
                               description = f'{ctx.author.mention} Bitte nenne einen User den du Bannen möchtest.\n\nNutzung: `zae!ban <@Nutzer / ID> [Grund]`\n\n\n**`Hinweis: <> makierte Argumente sind notwendig, [] makierte Argumente sind optional`**')
            em.set_footer(text = f"User-ID: {ctx.author.id}" , icon_url = f"{ctx.author.display_avatar}")
            em.set_author(name = f'{ctx.author}' , icon_url = f'{ctx.author.display_avatar}')
            return await ctx.reply(embed = em , mention_author = True)
        elif isinstance(user , discord.Member):
            if member.top_role.position < ctx.author.top_role.position:
                await ctx.guild.ban(user , reason = f"{reason}")
                embed = discord.Embed(timestamp = ctx.message.created_at , color = 0xff2200 ,
                                      title = ":hammer: Nutzer gebannt" ,
                                      description = f"**Gebannter Nutzer: {user}**\n**Moderator: {ctx.author}**\n**Grund: {reason}**")
                embed.set_footer(text = f"User-ID: {user.id}" , icon_url = ctx.author.display_avatar)
                embed.set_author(name = f"{ctx.author}" , icon_url = ctx.author.display_avatar)
                return await ctx.reply(embed = embed , mention_author = True)
            else:
                embed = discord.Embed(timestamp = ctx.message.created_at , title = "Fehler aufgetreten" ,
                                      description = f"Du kannst diesen Nutzer nicht bannen, weil du laut der Rollen Hierachie zu niedrig bist")
                embed.set_footer(text = f"User-ID: {ctx.author.id}" , icon_url = ctx.author.display_avatar)
                embed.set_author(name = f"{ctx.author}" , icon_url = ctx.author.display_avatar)
                return await ctx.reply(embed = embed , mention_author = True)
        elif isinstance(user , discord.User):
            await ctx.guild.ban(user , reason = f"{reason}")
            embed = discord.Embed(timestamp = ctx.message.created_at , color = 0xff2200 , title = "🔨 Nutzer gebannt" ,
                                  description = f"**Gebannter Nutzer:** {user}\n**Moderator:** {ctx.author}\n**Grund: {reason}**")
            embed.set_footer(text = f"User-ID: {user.id}" , icon_url = ctx.author.display_avatar)
            embed.set_author(name = f"{ctx.author}" , icon_url = ctx.author.display_avatar)
            return await ctx.reply(embed = embed , mention_author = True)

    @ban.error
    async def on_command_error(self , ctx , error):
        if isinstance(error , commands.MemberNotFound):
            return await ctx.reply(f"{ctx.author} der Nutzer konnte nicht gefunden werden!" , mention_author = True)
        elif isinstance(error , commands.UserNotFound):
            return await ctx.reply(f"{ctx.author} der Nutzer konnte nicht gefunden werden!" , mention_author = True)
        elif isinstance(error , commands.MissingPermissions):
            print(
                f"[OnCommandError - MissingPermissions] {ctx.author} - {ctx.author.id} hat für den Ban Command keine Berechtigung!")
            return await ctx.send(f"{ctx.author} du hast nicht die `BAN_MEMBERS` Berechtigung!")
        elif isinstance(error , commands.BotMissingPermissions):
            print(
                f"[OnCommandError - BotMissingPermissions] {ctx.author} - {ctx.author.id} hat mir keine Berechtigung für den Ban Command gegeben!")
            return await ctx.send(f"{ctx.author} ich habe nicht die `BAN_MEMBERS` Berechtigung!")
        elif isinstance(error , commands.CommandInvokeError):
            embed = discord.Embed(timestamp = ctx.message.created_at , title = "Fehler aufgetreten" ,
                                  description = "Der Fehler ist aus mehreren möglichen Gründen entstanden!\n\nDu bist zu niedrig von der Rollen-Hierarchie, um dies zu tun\n\nDer Nutzer, den du bannen wolltest ist bereits gebannt\n\nIch habe keine Berechtigung, um dies zu tun\n\nDu hast keine Berechtigung, um dies zu tun")
            embed.set_footer(text = f"User-ID: {ctx.author.id}" , icon_url = ctx.author.display_avatar)
            embed.set_author(name = f"{ctx.author}" , icon_url = ctx.author.display_avatar)
            return await ctx.reply(embed = embed , mention_author = True)
        else:
            raise error

    @commands.command(aliases = ['blist' , 'ban-list'])
    @commands.guild_only()
    @commands.has_guild_permissions(ban_members = True)
    @commands.bot_has_guild_permissions(ban_members = True)
    async def banlist(self , ctx):
        bans = await ctx.guild.bans()
        loop = [f"{u[1]} ({u[1].id})" for u in bans]
        _list = "\r\n".join([f"[{str(num).zfill(2)}] {data}" for num , data in enumerate(loop , start = 1)])
        embed = discord.Embed(timestamp = ctx.message.created_at , color = discord.Colour.random() ,
                              title = f"Banliste von {ctx.guild.name}" ,
                              description = f"```swift\n{_list}\n```")
        embed.set_author(name = f'{ctx.author}' , icon_url = ctx.message.author.display_avatar)
        embed.set_footer(text = f'User-ID: {ctx.author.id}' , icon_url = ctx.message.author.display_avatar)
        return await ctx.reply(embed = embed , mention_author = False)

    @banlist.error
    async def banlist_error(self , ctx , error):
        if isinstance(error , commands.CommandInvokeError):
            return await ctx.reply(
                f"{ctx.author.mention} es sind zu viele gebannte User auf dem Server, dass ich das nicht anzeigen kann! :/" ,
                mention_author = True)
        elif isinstance(error , commands.BotMissingPermissions):
            return await ctx.reply(
                f"{ctx.author.mention} ich kann die Bannliste nicht fetchen! Grund: Ich habe nicht die `BAN_MEMBERS` Berechtigung!" ,
                mention_author = True)
        elif isinstance(error , commands.MissingPermissions):
            return await ctx.reply(
                f"{ctx.author.mention} ich kann dir die Bannliste nicht anzeigen! Grund: Du hast nicht die `BAN_MEMBERS` Berechtigung!" ,
                mention_author = True)
        else:
            raise error

    @commands.command(aliases = ['kickid'])
    @commands.has_guild_permissions(kick_members = True)
    @commands.bot_has_guild_permissions(kick_members = True)
    @commands.guild_only()
    async def kick(self , ctx , member: discord.Member = None , * , reason='Kein Grund angegeben'):
        if member is None:
            em = discord.Embed(timestamp = ctx.message.created_at , color = 0xff2200 , title = "Argumente Fehlen" ,
                               description = f'{ctx.author.mention} Bitte nenne einen User den du Kicken möchtest.\n\n`zae!kick (@nutzer / id) [(optional) Grund]`')
            em.set_author(name = f'{ctx.author}' , icon_url = ctx.message.author.display_avatar)
            return await ctx.reply(embed = em , mention_author = True)
        else:
            await ctx.guild.kick(member , reason = reason)
            embe = discord.Embed(timestamp = ctx.message.created_at , color = 0xff2200 , title = "Kick ausgeführt!")
            embed.add_field(name = "Betroffener Nutzer:" , value = f"{member}\n**ID:**\n{member.id}" , inline = True)
            embed.add_field(name = "Moderator:" , value = f"{ctx.author}\n**ID:**\n{ctx.author.id}" , inline = True)
            embed.add_field(name = "Grund:" , value = str(reason) , inline = True)
            embe.set_author(name = f'{ctx.author}' , icon_url = ctx.message.author.display_avatar)
            embe.set_footer(text = 'User-ID: ' + str(member.id) , icon_url = ctx.message.author.display_avatar)
            return await ctx.reply(embed = embe , mention_author = False)

    @kick.error
    async def kick_error(self , ctx , error):
        if isinstance(error , commands.MissingPermissions):
            print(
                f"[OnCommandError - MissingPermissions] {ctx.author} - {ctx.author.id} hat für den Kick Command keine Berechtigung!")
            return await ctx.send(
                f"[OnCommandError - MissingPermissions] {ctx.author} du hast nicht die `Kick_Members` Berechtigung!")
        elif isinstance(error , commands.BotMissingPermissions):
            print(
                f"[OnCommandError - BotMissingPermissions] {ctx.author} - {ctx.author.id} hat mir keine Berechtigung für den Kick Command gegeben!")
            return await ctx.send(
                f"[OnCommandError - BotMissingPermissions] {ctx.author} ich habe nicht die `Kick_Members` Berechtigung!")
        elif isinstance(error , commands.MemberNotFound):
            return await ctx.send(
                f"[OnCommandError - MemberNotFound] {ctx.author} bist du dir sicher, dass der Nutzer hier auf diesem Server existiert? 🤔")
        else:
            pass

    @commands.command(aliases = ['lock'])
    @commands.guild_only()
    @commands.has_guild_permissions(manage_channels = True)
    @commands.bot_has_guild_permissions(manage_channels = True)
    async def lockdown(self , ctx , channel: discord.TextChannel = None):
        if channel is not None:
            await channel.set_permissions(ctx.guild.default_role, send_messages = False)
            embed = discord.Embed(timestamp = ctx.message.created_at , color = 0xff2200 , title = "Kanal gesperrt" ,
                                  description = f"Der Kanal {channel.mention} wurde von {ctx.author} gesperrt!")
            embed.set_author(name = f'{ctx.author}' , icon_url = ctx.message.author.display_avatar)
            return await ctx.reply(embed = embed , mention_author = False)
        else:
            return await ctx.reply("Du musst schon einen Text-Kanal erwähnen!" , mention_author = True)

    @lockdown.error
    async def lockdown_error(self , ctx , error):
        if isinstance(error , commands.MissingPermissions):
            print(
                f"[OnCommandError - MissingPermissions] {ctx.author} - {ctx.author.id} hat für den Lockup Command keine Berechtigung!")
            return await ctx.send(f"{ctx.author} du hast nicht die `Manage_Channels` Berechtigung!")
        elif isinstance(error , commands.BotMissingPermissions):
            print(
                f"[OnCommandError - BotMissingPermissions] {ctx.author} - {ctx.author.id} hat mir keine Berechtigung für den Lockup Command gegeben!")
            return await ctx.send(f"{ctx.author} ich habe nicht die `Manage_Channels` Berechtigung!")
        elif isinstance(error , commands.CommandInvokeError):
            return await ctx.send(f"{ctx.author} der Kanal konnte auf diesem Server nicht gefunden werden!")
        else:
            raise error

    @commands.command(aliases = ['unlock'])
    @commands.guild_only()
    @commands.has_guild_permissions(manage_channels = True)
    @commands.bot_has_guild_permissions(manage_channels = True)
    async def lockup(self , ctx , channel: discord.TextChannel = None):
        if channel is not None:
            await channel.set_permissions(ctx.guild.default_role , send_messages = True)
            embed = discord.Embed(timestamp = ctx.message.created_at , color = 0xff2200 ,
                                  title = "Kanal entsperrt" ,
                                  description = f"Der Kanal {channel.mention} wurde von {ctx.author} entsperrt!")
            embed.set_author(name = f'{ctx.author}' , icon_url = ctx.message.author.display_avatar)
            return await ctx.reply(embed = embed , mention_author = False)
        else:
            return await ctx.reply("Du musst schon einen Text-Kanal erwähnen!" , mention_author = True)

    @lockup.error
    async def lockup_error(self , ctx , error):
        if isinstance(error , commands.MissingPermissions):
            print(
                f"[OnCommandError - MissingPermissions] {ctx.author} - {ctx.author.id} hat für den Lockup Command keine Berechtigung!")
            await ctx.send(f"{ctx.author} du hast nicht die `Manage_Channels` Berechtigung!")
        elif isinstance(error , commands.BotMissingPermissions):
            print(
                f"[OnCommandError - BotMissingPermissions] {ctx.author} - {ctx.author.id} hat mir keine Berechtigung für den Lockup Command gegeben!")
            await ctx.send(f"{ctx.author} ich habe nicht die `Manage_Channels` Berechtigung!")
        else:
            pass

    @commands.command(aliases = ['unm'])
    @commands.guild_only()
    @commands.has_permissions(manage_messages = True)
    @commands.bot_has_guild_permissions(manage_roles = True)
    async def unmute(self , ctx , member: discord.Member , * , reason="Kein Grund angegeben"):
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles , name = "Muted")
        user_roles = member.roles
        if member.id == ctx.author.id:
            embed = discord.Embed(timestamp = ctx.message.created_at , color = 0xff2200 ,
                                  title = "Fehler!" ,
                                  description = "Aktion konnte nicht ausgeführt werden! Grund: Du kannst dich selbst nicht entmuten!")
            embed.set_author(name = f"{ctx.author}" , icon_url = ctx.message.author.display_avatar)
            embed.set_footer(text = f'User-ID: {ctx.author.id}')
            return await ctx.reply(embed = embed , mention_author = True)
        elif mutedRole not in user_roles:
            return await ctx.reply("Der Nutzer ist nicht gemuted!")
        else:
            embed = discord.Embed(title = "Unmute ausgeführt" ,
                                  colour = discord.Colour.random())
            embed.add_field(name = "Betroffener Nutzer:" , value = f"{member}\n**ID:**\n{member.id}" , inline = True)
            embed.add_field(name = "Moderator:" , value = f"{ctx.author}\n**ID:**\n{ctx.author.id}" , inline = True)
            embed.add_field(name = "Grund:" , value = str(reason) , inline = True)
            await member.remove_roles(mutedRole , reason = reason)
            return await ctx.reply(embed = embed)

    @commands.command(aliases = ['temp-mute'])
    @commands.guild_only()
    @commands.has_guild_permissions(manage_messages = True)
    @commands.bot_has_guild_permissions(manage_channels = True , manage_threads = True , manage_roles = True)
    async def tempmute(self , ctx , user: discord.Member , duration=0 , unit=None , * , reason=None):
        guild = ctx.guild
        name = ["Muted" , "muted" , "Knast" , "Mute" , "mute" , "Stumm geschaltet" , "knast" , "stumm geschaltet"]
        Muted = discord.utils.get(guild.roles , name = name)
        if user.id == ctx.author.id:
            embed = discord.Embed(timestamp = ctx.message.created_at , color = 0xff2200 ,
                                  title = "Fehler!" ,
                                  description = "Aktion konnte nicht ausgeführt werden! Grund: Du kannst dich selbst nicht muten!")
            embed.set_author(name = f"{ctx.author}" , icon_url = ctx.author.display_avatar)
            embed.set_footer(text = f'User-ID: {ctx.author.id}', icon_url = ctx.author.display_avatar)
            return await ctx.reply(embed = embed , mention_author = True)
        elif not Muted:
            perms = discord.Permissions(send_messages = False , add_reactions = False ,
                                        create_private_threads = False , create_public_threads = False ,
                                        manage_threads = False , send_messages_in_threads = False ,
                                        connect = False , speak = False)
            Muted = await guild.create_role(name = "Muted" , permissions = perms)
        for channel in guild.text_channels:
            try:
                await channel.set_permissions(Muted , send_messages = False , add_reactions = False ,
                                              create_private_threads = False , create_public_threads = False ,
                                              manage_threads = False , send_messages_in_threads = False)
            except Exception:
                pass
        for channel in guild.voice_channels:
            try:
                await channel.set_permissions(Muted , connect = False , speak = False)
                await user.add_roles(Muted , reason = reason)
            except Exception:
                pass
        await ctx.reply(f":white_check_mark: {user} stummgeschaltet für {duration}{unit}\n Grund: {reason}" ,
                        delete_after = 3)
        await user.add_roles(Muted , reason = reason)
        if unit == "s":
            wait = 1 * duration
            await asyncio.sleep(wait)
        elif unit == "m":
            wait = 60 * duration
            await asyncio.sleep(wait)
        elif unit == "h":
            wait = 60 * 60 * duration
            await asyncio.sleep(wait)
        elif duration == "d":
            wait = seconds * 86400
            await asyncio.sleep(wait)
        else:
            pass
        await user.remove_roles(Muted , reason = "Temp-Mute is over!")
        unmute_embed = discord.Embed(timestamp = ctx.message.created_at , title = "Tempmute vorbei!")
        unmute_embed.add_field(name = "Betroffener Nutzer:" , value = f"{member}\n**ID:**\n{member.id}" , inline = True)
        unmute_embed.add_field(name = "Moderator:" , value = f"{ctx.author}\n**ID:**\n{ctx.author.id}" , inline = True)
        unmute_embed.add_field(name = "Grund:" , value = str(reason) , inline = True)
        return await ctx.reply(embed = unmute_embed)

    @tempmute.error
    async def tempmute_error(self , ctx , error):
        if isinstance(error , commands.BotMissingPermissions):
            embed = discord.Embed(timestamp = ctx.message.created_at , color = 0xff2200 ,
                                  title = "Fehlende Berechtigungen!" ,
                                  description = "Aktion konnte nicht ausgeführt werden! Grund: Ich benötige die Berechtigungen `manage_roles` und `manage_channels`, um diese Aktion auszuführen\n\nManage_Roles wird benötigt, um dem Benutzer die Muted Rolle zu geben!\nManage_Channels wird benötigt, falls ich eine Muted Rolle erstellen muss und um die Berechtigungen der Rolle innerhalb der Kanäle zu ändern, um sicherzustellen, dass die stummgeschaltete Person nirgendwo schreiben darf (wenn ich keine Muted Rolle finde und der Benutzer kein Administrator ist)")
            embed.set_author(name = f"{ctx.author}" , icon_url = ctx.author.display_avatar)
            embed.set_footer(text = f'User-ID: {ctx.author.id}', icon_url = ctx.author.display_avatar)
            return await ctx.reply(embed = embed , mention_author = True)
        elif isinstance(error , commands.MissingPermissions):
            embed = discord.Embed(timestamp = ctx.message.created_at , color = 0xff2200 ,
                                  title = "Fehlende Berechtigungen!" ,
                                  description = "Aktion konnte nicht ausgeführt werden! Grund: Du benötigst die Berechtigungen `manage_roles`, um diese Aktion auszuführen")
            embed.set_author(name = f"{ctx.author}" , icon_url = ctx.author.display_avatar)
            embed.set_footer(text = f'User-ID: {ctx.author.id}')
            return await ctx.reply(embed = embed , mention_author = True)
        else:
            raise error

    @commands.command(description = "Mutes the specified user.")
    @commands.guild_only()
    @commands.has_permissions(manage_roles = True , manage_channels = True , manage_threads = True)
    async def mute(self , ctx , member: discord.Member , * , reason="Kein Grund angegeben"):
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles , name = "Muted")
        user_roles = member.roles
        if member.id == ctx.author.id:
            embed = discord.Embed(timestamp = ctx.message.created_at , color = 0xff2200 ,
                                  title = "Fehler!" ,
                                  description = "Aktion konnte nicht ausgeführt werden! Grund: Du kannst dich selbst nicht muten!")
            embed.set_author(name = f"{ctx.author}" , icon_url = ctx.author.display_avatar)
            embed.set_footer(text = f'User-ID: {ctx.author.id}', icon_url = ctx.author.display_avatar)
            return await ctx.reply(embed = embed , mention_author = True)
        elif member.top_role > ctx.author.top_role:
            embed = discord.Embed(timestamp = ctx.message.created_at , color = 0xff2200 ,
                                  title = "Fehler!" ,
                                  description = "Aktion konnte nicht ausgeführt werden! Grund: Du kannst niemanden stummschalten, der höher als du ist!")
            embed.set_author(name = f"{ctx.author}" , icon_url = ctx.author.display_avatar)
            embed.set_footer(text = f'User-ID: {ctx.author.id}', icon_url = ctx.author.display_avatar)
            return await ctx.reply(embed = embed , mention_author = True)
        if not mutedRole:
            mutedRole = await guild.create_role(name = "Muted" , mentionable = False , hoist = False ,
                                                color = 0xffffff ,
                                                reason = "Muted Rolle nicht gefunden, wird erstellt und eingestellt...")
            embed1 = discord.Embed(timestamp = ctx.message.created_at , title = "Muted Rolle" ,
                                   description = "Muted Rolle wird erstellt und eingestellt\n\nGrund: Die Muted Rolle wurde nicht gefunden" ,
                                   colour = discord.Colour.random())
            message = await ctx.reply(embed = embed1)
            for channel in guild.channels:
                await channel.set_permissions(mutedRole , connect = False , speak = False , send_messages = False ,
                                              create_private_threads = False , create_public_threads = False ,
                                              send_messages_in_threads = False , create_instant_invite = False ,
                                              add_reactions = False)
            embed2 = discord.Embed(timestamp = ctx.message.created_at , title = "Mute ausgeführt" ,
                                   colour = discord.Colour.random() ,
                                   description = "**HINWEIS:** Die Muted Rolle 'Muted' benannt lassen, sonst gibt es Schwierigkeiten bei den Rollen, für die weder ich noch der Entwickler verantwortlich sind!")
            embed2.add_field(name = "Betroffener Nutzer:" , value = f"{member}\n\n**ID:**\n{member.id}" , inline = True)
            embed2.add_field(name = "Moderator:" , value = f"{ctx.author}\n\n**ID:**\n{ctx.author.id}" , inline = True)
            embed2.add_field(name = "Grund:" , value = str(reason) , inline = True)
            await member.add_roles(mutedRole , reason = reason)
            await message.edit(embed = embed2)
        elif mutedRole in user_roles:
            embed = discord.Embed(timestamp = ctx.message.created_at , title = "Nutzer ist bereits gemuted" ,
                                  colour = 0xff0000)
            embed.add_field(name = "Nutzer:" , value = f"{member}\n\n**ID:**\n{member.id}" , inline = False)
            return await ctx.reply(embed = embed)
        else:
            embed = discord.Embed(timestamp = ctx.message.created_at , title = "Mute ausgeführt" ,
                                  colour = discord.Colour.random() ,
                                  description = "**HINWEIS:** Die Muted Rolle 'Muted' benannt lassen, sonst gibt es Schwierigkeiten bei den Rollen, für die weder ich noch mein Entwickler verantwortlich sind!")
            embed.add_field(name = "Betroffener Nutzer:" , value = f"{member}\n\n**ID:**\n{member.id}" , inline = True)
            embed.add_field(name = "Moderator:" , value = f"{ctx.author}\n\n**ID:**\n{ctx.author.id}" , inline = True)
            embed.add_field(name = "Grund:" , value = str(reason) , inline = True)
            await member.add_roles(mutedRole , reason = reason)
            return await ctx.reply(embed = embed)

    @mute.error
    async def mute_error(self , ctx , error):
        if isinstance(error , commands.BotMissingPermissions):
            embed = discord.Embed(timestamp = ctx.message.created_at , color = 0xff2200 ,
                                  title = "Fehlende Berechtigungen!" ,
                                  description = "Aktion konnte nicht ausgeführt werden! Grund: Ich benötige die Berechtigungen `manage_roles` und `manage_channels`, um diese Aktion auszuführen\n\nManage_Roles wird benötigt, um dem Benutzer die Muted Rolle zu geben!\nManage_Channels wird benötigt, falls ich eine Muted Rolle erstellen muss und um die Berechtigungen der Rolle innerhalb der Kanäle zu ändern, um sicherzustellen, dass die stummgeschaltete Person nirgendwo schreiben darf (wenn ich keine Muted Rolle finde und der Benutzer kein Administrator ist)")
            embed.set_author(name = f"{ctx.author}" , icon_url = ctx.author.display_avatar)
            embed.set_footer(text = f'User-ID: {ctx.author.id}')
            return await ctx.reply(embed = embed , mention_author = True)
        elif isinstance(error , commands.MissingPermissions):
            embed = discord.Embed(timestamp = ctx.message.created_at , color = 0xff2200 ,
                                  title = "Fehlende Berechtigungen!" ,
                                  description = "Aktion konnte nicht ausgeführt werden! Grund: Du benötigst die Berechtigungen `manage_roles`, um diese Aktion auszuführen")
            embed.set_author(name = f"{ctx.author}" , icon_url = ctx.author.display_avatar)
            embed.set_footer(text = f'User-ID: {ctx.author.id}')
            return await ctx.reply(embed = embed , mention_author = True)
        elif isinstance(error , commands.MemberNotFound):
            embed = discord.Embed(timestamp = ctx.message.created_at , color = 0xff2200 ,
                                  title = "Fehler!" ,
                                  description = "Aktion konnte nicht ausgeführt werden! Grund: Der Nutzer konnte nicht gefunden werden!")
            embed.set_author(name = f"{ctx.author}" , icon_url = ctx.author.display_avatar)
            embed.set_footer(text = f'User-ID: {ctx.author.id}')
            return await ctx.reply(embed = embed , mention_author = True)
        else:
            raise error

    @commands.command(description = "Mutes the specified user.")
    @commands.guild_only()
    @commands.has_permissions(manage_roles = True , manage_channels = True , manage_threads = True)
    async def massmute(self , ctx , member: commands.Greedy[discord.Member] , * , reason="Kein Grund angegeben"):
        user = 0
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles , name = "Muted")
        if not mutedRole:
            mutedRole = await guild.create_role(name = "Muted" , mentionable = False , hoist = False ,
                                                color = 0xffffff ,
                                                reason = "Muted Rolle nicht gefunden, wird erstellt und eingestellt...")
            for channel in guild.channels:
                await channel.set_permissions(mutedRole , connect = False , speak = False , send_messages = False ,
                                              create_private_threads = False , create_public_threads = False ,
                                              send_messages_in_threads = False , create_instant_invite = False ,
                                              add_reactions = False)
            for x in member:
                try:
                    user += 1
                    await x.add_roles(mutedRole , reason = reason)
                except Exception as e:
                    print(e)
                    pass
            embed = discord.Embed(timestamp = ctx.message.created_at , color = 0xff2200 ,
                                  title = "Massmute ausgeführt :tools:" ,
                                  description = f"**{user}** Personen wurden gemuted.")
            embed.set_footer(text = f"User-ID: {ctx.author.id}" , icon_url = ctx.author.display_avatar)
            embed.set_author(name = f"{ctx.author}" , icon_url = ctx.author.display_avatar)
            return await ctx.reply(embed = embed, mention_author = False)
        else:
            for x in member:
                try:
                    user += 1
                    await x.add_roles(mutedRole , reason = reason)
                except Exception as e:
                    print(e)
                    pass
            embed = discord.Embed(timestamp = ctx.message.created_at , color = 0xff2200 ,
                                  title = "Massmute ausgeführt :tools:" ,
                                  description = f"**{user}** Personen wurden gemuted.")
            embed.set_footer(text = f"User-ID: {ctx.author.id}" , icon_url = ctx.author.display_avatar)
            embed.set_author(name = f"{ctx.author}" , icon_url = ctx.author.display_avatar)
            return await ctx.reply(embed = embed , mention_author = False)

    @massmute.error
    async def mute_error(self , ctx , error):
        if isinstance(error , commands.BotMissingPermissions):
            embed = discord.Embed(timestamp = ctx.message.created_at , color = 0xff2200 ,
                                  title = "Fehlende Berechtigungen!" ,
                                  description = "Aktion konnte nicht ausgeführt werden! Grund: Ich benötige die Berechtigungen `manage_roles` und `manage_channels`, um diese Aktion auszuführen\n\nManage_Roles wird benötigt, um dem Benutzer die Muted Rolle zu geben!\nManage_Channels wird benötigt, falls ich eine Muted Rolle erstellen muss und um die Berechtigungen der Rolle innerhalb der Kanäle zu ändern, um sicherzustellen, dass die stummgeschaltete Person nirgendwo schreiben darf (wenn ich keine Muted Rolle finde und der Benutzer kein Administrator ist)")
            embed.set_author(name = f"{ctx.author}" , icon_url = ctx.author.display_avatar)
            embed.set_footer(text = f'User-ID: {ctx.author.id}', icon_url = ctx.author.display_avatar)
            return await ctx.reply(embed = embed , mention_author = True)
        elif isinstance(error , commands.MissingPermissions):
            embed = discord.Embed(timestamp = ctx.message.created_at , color = 0xff2200 ,
                                  title = "Fehlende Berechtigungen!" ,
                                  description = "Aktion konnte nicht ausgeführt werden! Grund: Du benötigst die Berechtigungen `manage_roles`, um diese Aktion auszuführen")
            embed.set_author(name = f"{ctx.author}" , icon_url = ctx.author.display_avatar)
            embed.set_footer(text = f'User-ID: {ctx.author.id}')
            return await ctx.reply(embed = embed , mention_author = True)
        elif isinstance(error , commands.MemberNotFound):
            embed = discord.Embed(timestamp = ctx.message.created_at , color = 0xff2200 ,
                                  title = "Fehler!" ,
                                  description = "Aktion konnte nicht ausgeführt werden! Grund: Der Nutzer konnte nicht gefunden werden!")
            embed.set_author(name = f"{ctx.author}" , icon_url = ctx.author.display_avatar)
            embed.set_footer(text = f'User-ID: {ctx.author.id}')
            return await ctx.reply(embed = embed , mention_author = True)
        else:
            raise error

    @commands.command(description = "Mutes the specified user.")
    @commands.guild_only()
    @commands.has_permissions(manage_roles = True , manage_channels = True , manage_threads = True)
    async def massunmute(self , ctx , member: commands.Greedy[discord.Member] , * , reason="Kein Grund angegeben"):
        user = 0
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles , name = "Muted")
        if not mutedRole:
            mutedRole = await guild.create_role(name = "Muted" , mentionable = False , hoist = False ,
                                                color = 0xffffff ,
                                                reason = "Muted Rolle nicht gefunden, wird erstellt und eingestellt...")
            for channel in guild.channels:
                await channel.set_permissions(mutedRole , connect = False , speak = False , send_messages = False ,
                                              create_private_threads = False , create_public_threads = False ,
                                              send_messages_in_threads = False , create_instant_invite = False ,
                                              add_reactions = False)
            for x in member:
                try:
                    user += 1
                    await x.remove_roles(mutedRole , reason = reason)
                except Exception:
                    pass
            embed = discord.Embed(timestamp = ctx.message.created_at , color = 0xff2200 ,
                                  title = "Massmute ausgeführt :tools:" ,
                                  description = f"**{user}** Personen wurden entmuted.")
            embed.set_footer(text = f"User-ID: {ctx.author.id}" , icon_url = ctx.author.display_avatar)
            embed.set_author(name = f"{ctx.author}" , icon_url = ctx.author.display_avatar)
            return await ctx.reply(embed = embed , mention_author = False)
        else:
            for x in member:
                try:
                    user += 1
                    await x.remove_roles(mutedRole , reason = reason)
                except Exception:
                    pass
            embed = discord.Embed(timestamp = ctx.message.created_at , color = 0xff2200 ,
                                  title = "Massunmute ausgeführt :tools:" ,
                                  description = f"**{user}** Personen wurden entmuted.")
            embed.set_footer(text = f"User-ID: {ctx.author.id}" , icon_url = ctx.author.display_avatar)
            embed.set_author(name = f"{ctx.author}" , icon_url = ctx.author.display_avatar)
            return await ctx.reply(embed = embed , mention_author = False)

    @commands.command(aliases=["addrole", "arole", "grole", "give-role", "g_role", "gr", "ar"])
    @commands.guild_only()
    @commands.bot_has_guild_permissions(manage_roles = True)
    @commands.has_guild_permissions(manage_roles = True)
    async def giverole(self, ctx, member: discord.Member = None, *, role: discord.Role = None):
        if member is None:
            em = discord.Embed(timestamp = ctx.message.created_at , color = 0xff2200 , title = "Argumente Fehlen" ,
                               description = f'{ctx.author.mention} Bitte nenne ein Mitglied dem du eine Rolle geben möchtest.\n\n`zae!giverole (@nutzer / nutzer-id) (@rolle / rollen-id) [(optional) Grund]`')
            em.set_author(name = f'{ctx.author}' , icon_url = ctx.author.display_avatar)
            return await ctx.reply(embed = em , mention_author = True)
        elif role is None:
            embed = discord.Embed(timestamp = ctx.message.created_at , color = 0xff2200 , title = "Argumente Fehlen" ,
                                  description = f'{ctx.author.mention} Bitte nenne eine Rolle welche du {member} geben möchtest.\n\n`zae!giverole (@nutzer / nutzer-id) (@rolle / rollen-id)`')
            embed.set_author(name = ctx.author , icon_url = ctx.author.display_avatar)
            return await ctx.reply(embed = embed , mention_author = True)
        elif ctx.author.guild_permissions.manage_roles:
            if member.top_role > ctx.author.top_role:
                embed = discord.Embed(timestamp = ctx.message.created_at, color = 0xff2200, title = "Fehler!",
                                      description = f"{ctx.author} du bist von der Rollen-Hierarchie zu niedrig, um diese Aktion auszuführen!")
                embed.set_author(name = ctx.author, icon_url = ctx.author.display_avatar)
                return await ctx.reply(embed=embed, mention_author = True)
            elif role > ctx.author.top_role:
                embed = discord.Embed(timestamp = ctx.message.created_at , color = 0xff2200 , title = "Fehler!" ,
                                      description = f"{ctx.author} du bist von der Rollen-Hierarchie zu niedrig, um diese Aktion auszuführen!")
                embed.set_author(name = ctx.author , icon_url = ctx.author.display_avatar)
                return await ctx.reply(embed = embed , mention_author = True)
            else:
                embed = discord.Embed(timestamp = ctx.message.created_at, title = "Rolle gegeben ✅",
                                      color=discord.Colour.random())
                embed.add_field(name = "Nutzer", value = f"{member.mention}\n{member}\n{member.id}", inline = True)
                embed.add_field(name = "Moderator", value = f"{ctx.author.mention}\n{ctx.author}\n{ctx.author.id}", inline = True)
                embed.add_field(name = "Rolle", value = f"{role.mention}\n`{role.name}`\n`{role.id}`", inline = True)
                embed.set_author(name = ctx.author , icon_url = ctx.author.display_avatar)
                await member.add_roles(role)
                return await ctx.reply(embed=embed, mention_author = True)
        else:
            embed = discord.Embed(timestamp = ctx.message.created_at , title = "Fehler!" ,
                                  description = f"{ctx.author} du hast keine Berechtigung für diesen Command! [MANAGE_ROLES]" ,
                                  color = discord.Colour.random())
            return await ctx.reply(embed = embed , mention_author = True)
        if self.zeus.guild_permissions.manage_roles:
            if member.top_role > self.zeus.top_role:
                embed = discord.Embed(timestamp = ctx.message.created_at, color = 0xff2200, title = "Fehler!",
                                      description = f"{ctx.author} ich bin von der Rollen-Hierarchie zu niedrig, um diese Aktion auszuführen!")
                embed.set_author(name = ctx.author, icon_url = ctx.author.display_avatar)
                return await ctx.reply(embed=embed, mention_author = True)
            elif role > self.zeus.top_role:
                embed = discord.Embed(timestamp = ctx.message.created_at, color = 0xff2200, title = "Fehler!",
                                      description = f"{ctx.author} ich bin von der Rollen-Hierarchie zu niedrig, um diese Aktion auszuführen!")
                embed.set_author(name = ctx.author, icon_url = ctx.author.display_avatar)
                return await ctx.reply(embed=embed, mention_author = True)
            else:
                embed = discord.Embed(timestamp = ctx.message.created_at, title = "Rolle gegeben ✅",
                                      color=discord.Colour.random())
                embed.add_field(name = "Nutzer", value = f"{member.mention}\n{member}\n{member.id}", inline = True)
                embed.add_field(name = "Moderator", value = f"{ctx.author.mention}\n{ctx.author}\n{ctx.author.id}", inline = True)
                embed.add_field(name = "Rolle", value = f"{role.mention}\n`{role.name}`\n`{role.id}`", inline = True)
                await member.add_roles(role)
                return await ctx.reply(embed=embed, mention_author = True)
        else:
            embed = discord.Embed(timestamp = ctx.message.created_at , title = "Fehler!" ,
                                  description = f"{ctx.author} ich habe keine Berechtigung für diesen Command! [MANAGE_ROLES]" ,
                                  color = discord.Colour.random())
            return await ctx.reply(embed = embed , mention_author = True)

    @giverole.error
    async def giverole_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(timestamp = ctx.message.created_at , color = 0xff2200 , title = "Fehler!" ,
                                  description = f"{ctx.author} du bist von der Rollen-Hierarchie zu niedrig, um diese Aktion auszuführen!")
            embed.set_author(name = ctx.author , icon_url = ctx.author.display_avatar)
            return await ctx.reply(embed = embed , mention_author = True)
        elif isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(timestamp = ctx.message.created_at , color = 0xff2200 , title = "Fehler!" ,
                                  description = f"{ctx.author} ich bin von der Rollen-Hierarchie zu niedrig, um diese Aktion auszuführen!")
            embed.set_author(name = ctx.author , icon_url = ctx.author.display_avatar)
            return await ctx.reply(embed = embed , mention_author = True)
        elif isinstance(error, commands.RoleNotFound):
            embed = discord.Embed(timestamp = ctx.message.created_at , title = "Fehler!" ,
                                  description = f"{ctx.author} die Rolle konnte nicht gefunden werden!" ,
                                  color = discord.Colour.random())
            return await ctx.reply(embed = embed , mention_author = True)
        elif isinstance(error, commands.MemberNotFound):
            embed = discord.Embed(timestamp = ctx.message.created_at , title = "Fehler!" ,
                                  description = f"{ctx.author} der Nutzer konnte nicht gefunden werden!" ,
                                  color = discord.Colour.random())
            return await ctx.reply(embed = embed , mention_author = True)
        elif isinstance(error, commands.CommandInvokeError):
            pass
        else:
            pass

    @commands.command(aliases = ["removerole" , "rrole" , "trole" , "take-role" , "t_role" , "tr" , "rr"])
    @commands.guild_only()
    @commands.bot_has_guild_permissions(manage_roles = True)
    @commands.has_guild_permissions(manage_roles = True)
    async def takerole(self , ctx , member: discord.Member = None , * , role: discord.Role = None):
        if member is None:
            em = discord.Embed(timestamp = ctx.message.created_at , color = 0xff2200 , title = "Argumente Fehlen" ,
                               description = f'{ctx.author.mention} Bitte nenne ein Mitglied dem du eine Rolle entziehen möchtest.\n\n**Nutzung:**\n```yaml\nzae!takerole (@nutzer / nutzer-id) (@rolle / rollen-id)\n```')
            em.set_author(name = f'{ctx.author}' , icon_url = ctx.author.display_avatar)
            return await ctx.reply(embed = em , mention_author = True)
        elif role is None:
            embed = discord.Embed(timestamp = ctx.message.created_at , color = 0xff2200 , title = "Argumente Fehlen" ,
                                  description = f'{ctx.author.mention} Bitte nenne eine Rolle welche du {member} entziehen möchtest.\n\n**Nutzung:**\n```yaml\nzae!takerole (@nutzer / nutzer-id) (@rolle / rollen-id)\n```')
            embed.set_author(name = ctx.author , icon_url = ctx.author.display_avatar)
            return await ctx.reply(embed = embed , mention_author = True)
        elif ctx.author.guild_permissions.manage_roles:
            if member.top_role > ctx.author.top_role:
                embed = discord.Embed(timestamp = ctx.message.created_at , color = 0xff2200 , title = "Fehler!" ,
                                      description = f"{ctx.author} du besitzt nicht die nötigen Berechtigungen, um diese Aktion auszuführen!")
                embed.add_field(name="Benötigte Berechtigung:", value = "**`[MANAGE_ROLES]`**", inline = False)
                embed.set_author(name = ctx.author , icon_url = ctx.author.display_avatar)
                return await ctx.reply(embed = embed , mention_author = True)
            elif role > ctx.author.top_role:
                embed = discord.Embed(timestamp = ctx.message.created_at , color = 0xff2200 , title = "Fehler!" ,
                                      description = f"{ctx.author} du bist von der Rollen-Hierarchie zu niedrig, um diese Aktion auszuführen!")
                embed.set_author(name = ctx.author , icon_url = ctx.author.display_avatar)
                return await ctx.reply(embed = embed , mention_author = True)
            else:
                embed = discord.Embed(timestamp = ctx.message.created_at , title = "Rolle gegeben ✅" ,
                                      color = discord.Colour.random())
                embed.add_field(name = "Nutzer:" , value = f"{member.mention}\n{member}\n{member.id}" , inline = True)
                embed.add_field(name = "Moderator:" , value = f"{ctx.author.mention}\n{ctx.author}\n{ctx.author.id}" ,
                                inline = True)
                embed.add_field(name = "Rolle:" , value = f"{role.mention}\n`{role.name}`\n`{role.id}`" , inline = True)
                await member.remove_roles(role)
                return await ctx.reply(embed = embed , mention_author = True)
        else:
            embed = discord.Embed(timestamp = ctx.message.created_at , title = "Fehler!" ,
                                  description = f"{ctx.author} du hast keine Berechtigung für diesen Command! [MANAGE_ROLES]" ,
                                  color = discord.Colour.random())
            return await ctx.reply(embed = embed , mention_author = True)
        if self.zeus.guild_permissions.manage_roles:
            if member.top_role > self.zeus.top_role:
                embed = discord.Embed(timestamp = ctx.message.created_at , color = 0xff2200 , title = "Fehler!" ,
                                      description = f"{ctx.author} ich besitze nicht die nötigen Berechtigungen, um diese Aktion auszuführen!")
                embed.add_field(name = "Benötigte Berechtigung:" , value = "**`[MANAGE_ROLES]`**" , inline = False)
                embed.set_author(name = ctx.author , icon_url = ctx.author.display_avatar)
                return await ctx.reply(embed = embed , mention_author = True)
            elif role > self.zeus.top_role:
                embed = discord.Embed(timestamp = ctx.message.created_at , color = 0xff2200 , title = "Fehler!" ,
                                      description = f"{ctx.author} ich besitze nicht die nötigen Berechtigungen, um diese Aktion auszuführen!")
                embed.add_field(name = "Benötigte Berechtigung:" , value = "**`[MANAGE_ROLES]`**" , inline = False)
                embed.set_author(name = ctx.author , icon_url = ctx.author.display_avatar)
                return await ctx.reply(embed = embed , mention_author = True)
            else:
                embed = discord.Embed(timestamp = ctx.message.created_at , title = "Rolle entzogen ✅" ,
                                      color = discord.Colour.random())
                embed.add_field(name = "Nutzer:" , value = f"{member.mention}\n{member}\n{member.id}" , inline = True)
                embed.add_field(name = "Moderator:" , value = f"{ctx.author.mention}\n{ctx.author}\n{ctx.author.id}" ,
                                inline = True)
                embed.add_field(name = "Rolle:" , value = f"{role.mention}\n`{role.name}`\n`{role.id}`" , inline = True)
                await member.remove_roles(role)
                return await ctx.reply(embed = embed , mention_author = True)
        else:
            embed = discord.Embed(timestamp = ctx.message.created_at , color = 0xff2200 , title = "Fehler!" ,
                                  description = f"{ctx.author} ich besitze nicht die nötigen Berechtigungen, um diese Aktion auszuführen!")
            embed.add_field(name = "Benötigte Berechtigung:" , value = "**`[MANAGE_ROLES]`**" , inline = False)
            embed.set_author(name = ctx.author , icon_url = ctx.author.display_avatar)
            return await ctx.reply(embed = embed , mention_author = True)

    @takerole.error
    async def takerole_error(self , ctx , error):
        if isinstance(error , commands.MissingPermissions):
            embed = discord.Embed(timestamp = ctx.message.created_at , color = 0xff2200 , title = "Fehler!" ,
                                  description = f"{ctx.author} du bist von der Rollen-Hierarchie zu niedrig, um diese Aktion auszuführen!")
            embed.set_author(name = ctx.author , icon_url = ctx.author.display_avatar)
            return await ctx.reply(embed = embed , mention_author = True)
        elif isinstance(error , commands.BotMissingPermissions):
            embed = discord.Embed(timestamp = ctx.message.created_at , color = 0xff2200 , title = "Fehler!" ,
                                  description = f"{ctx.author} ich bin von der Rollen-Hierarchie zu niedrig, um diese Aktion auszuführen!")
            embed.set_author(name = ctx.author , icon_url = ctx.author.display_avatar)
            return await ctx.reply(embed = embed , mention_author = True)
        elif isinstance(error , commands.RoleNotFound):
            embed = discord.Embed(timestamp = ctx.message.created_at , title = "Fehler!" ,
                                  description = f"{ctx.author} die Rolle konnte nicht gefunden werden!" ,
                                  color = discord.Colour.random())
            return await ctx.reply(embed = embed , mention_author = True)
        elif isinstance(error , commands.MemberNotFound):
            embed = discord.Embed(timestamp = ctx.message.created_at , title = "Fehler!" ,
                                  description = f"{ctx.author} der Nutzer konnte nicht gefunden werden!" ,
                                  color = discord.Colour.random())
            return await ctx.reply(embed = embed , mention_author = True)
        elif isinstance(error , commands.CommandInvokeError):
            pass
        else:
            pass

    @commands.command(aliases = ["purge"])
    @commands.guild_only()
    @commands.has_guild_permissions(manage_messages = True)
    @commands.bot_has_guild_permissions(manage_messages = True)
    async def clear(self , ctx , amount: int = None):
        if amount is None:
            await ctx.reply(f"{ctx.author.name} bitte erwähne eine Nummer!")
        elif amount == 0:
            await ctx.reply(f"{ctx.author.name} 0 Nachrichten löschen? Denk nochmal nach!")
        else:
            await ctx.channel.purge(limit = amount)
            await ctx.send(f"{ctx.author} hat {amount} Nachricht(en) gelöscht" , delete_after = 2)

    @clear.error
    async def clear_error(self , ctx , error):
        if isinstance(error , commands.MissingPermissions):
            return await ctx.send(f"{ctx.author.mention} Berechtigungs-Fehler! [Gebrauchte Berechtigung: manage_messages]")
        elif isinstance(error , commands.BotMissingPermissions):
            return await ctx.send(f"{ctx.author.mention} Berechtigungs-Fehler! [Gebrauchte Berechtigung: manage_messages]")
        else:
            raise error

    @commands.command(aliases = ["multiban" , "mass-ban" , "multi-ban"])
    @commands.bot_has_permissions(ban_members = True)
    @commands.has_guild_permissions(ban_members = True)
    async def massban(self , ctx , targets: commands.Greedy[discord.User], *, grund="Kein Grund angegeben"):
        banlist = await ctx.guild.bans()
        banned = 0
        days = 0
        tries = 0
        failed = 0
        for x in targets:
            tries += 1
            if x in banlist:
                failed += 1
                banned -= 1
            else:
                try:
                    await ctx.guild.ban(x, reason = f"{grund}" , delete_message_days = days)
                    banned += 1
                except Exception:
                    failed += 1
        embed = discord.Embed(timestamp = ctx.message.created_at , color = 0xff2200 ,
                              title = "Massban ausgeführt :tools:" ,
                              description = f"Es wurde versucht, **{tries}** Personen zu bannen. Ergebnisse: \n**{banned}** Nutzer wurde/n gebannt. \n**{failed}** Nutzer konnte/n nicht gebannt werden.")
        embed.set_footer(text = f"User-ID: {ctx.author.id}" , icon_url = ctx.author.display_avatar)
        embed.set_author(name = f"{ctx.author}" , icon_url = ctx.author.display_avatar)
        return await ctx.reply(embed = embed , mention_author = False)

    @massban.error
    async def massban_error(self , ctx , error):
        if isinstance(error , commands.MissingPermissions):
            await ctx.send(f"{ctx.author.mention} Berechtigungs-Fehler! [Gebrauchte Berechtigung: ban_members]")
        elif isinstance(error , commands.BotMissingPermissions):
            await ctx.send(f"{ctx.author.mention} Berechtigungs-Fehler! [Gebrauchte Berechtigung: ban_members]")
        elif isinstance(error , commands.UserNotFound):
            pass
        else:
            raise error

    @commands.command(aliases = ["multiunban" , "mass-unban" , "multi-unban"])
    @commands.bot_has_permissions(ban_members = True)
    @commands.has_guild_permissions(ban_members = True)
    async def massunban(self , ctx , targets: commands.Greedy[discord.User] , * , grund="Kein Grund angegeben"):
        with ctx.channel.typing():
            banned = 0
            tries = 0
            failed = 0
            for user in targets:
                tries += 1
                try:
                    await ctx.guild.unban(user , reason = f"{grund}")
                    banned += 1
                except Exception as e:
                    failed += 1
                    print(e)
            embed = discord.Embed(timestamp = ctx.message.created_at , color = 0xff2200 ,
                                  title = "Massunban executed 🛠" ,
                                  description = f"Es wurde versucht {tries} Nutzer zu entbannen. Ergebnis: \n**{banned}** Nutzer wurden entbannt. \n**{failed}** konnten nicht entbannt werden.")
            embed.set_footer(text = f"User-ID: {ctx.author.id}" , icon_url = ctx.author.display_avatar)
            embed.set_author(name = f"{ctx.author}" , icon_url = ctx.author.display_avatar)
            return await ctx.reply(embed = embed , mention_author = False)

    @massunban.error
    async def massunban_error(self , ctx , error):
        if isinstance(error , commands.MissingPermissions):
            await ctx.send(f"{ctx.author.mention} a Permission's missing! [Needed Permission: ban_members]")
        elif isinstance(error , commands.BotMissingPermissions):
            await ctx.send(f"{ctx.author.mention} a Permission's missing! [Needed Permission: ban_members]")
        elif isinstance(error , commands.UserNotFound):
            pass
        else:
            pass


def setup(zeus):
    zeus.add_cog(mod(zeus))
