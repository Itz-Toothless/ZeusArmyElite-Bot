import discord
from discord.ext import commands


class message_logs(commands.Cog):
    def __init__(self , zeus):
        self.zeus = zeus

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            pass
        else:
            d1 = message.created_at
            embed = discord.Embed(title = "Nachrichten-Log" ,
                                  description = f"**Nachricht:**\n{message.content}" , color = 0xFF0000)
            embed.add_field(name = f"Gelöscht am:" , value = "**<t:{}:{}>**".format(int(d1.timestamp()) , 'F') ,
                            inline = False)
            embed.set_author(name = f"{message.author}", icon_url = f'{message.author.avatar.url}')
            embed.set_footer(text = f"Message-ID: {message.id}" , icon_url = f"{message.author.avatar.url}")
            embed.set_thumbnail(url = f"{message.author.avatar.url}")
            channel = await self.zeus.fetch_channel(904464166608330772)
            return await channel.send(embed = embed)

    @commands.Cog.listener()
    async def on_message_edit(self, message_before , message_after):
        if message_before.author.bot:
            pass
        elif message_before.content == message_after.content:
            pass
        else:
            d1 = message_before.created_at
            embed = discord.Embed(title = "Nachrichten-Log" ,
                                  description = f"**Nachricht zuvor:**\n{message_before.content}\n\n**Nachricht danach:**\n{message_after.content}" ,
                                  color = 0xFF0000)
            embed.add_field(name = f"Geändert am:" , value = "**<t:{}:{}>**".format(int(d1.timestamp()) , 'F') ,
                            inline = False)
            embed.add_field(name = f"Nachrichten-Link:" , value = f"[Link zur Nachricht]({message_after.jump_url})")
            embed.set_author(name = f"{message_after.author}" , icon_url = f'{message_after.author.avatar.url}')
            embed.set_footer(text = f"Message-ID: {message_before.id}" ,
                             icon_url = f"{message_after.author.avatar.url}")
            channel = await self.zeus.fetch_channel(904464132030484530)
            return await channel.send(embed = embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        d1 = member.created_at
        d2 = member.joined_at
        embed = discord.Embed(color = discord.Colour.random() ,
                              title = f"{member} ist {member.guild.name} beigetreten")
        embed.add_field(name = "Beigetreten am:" , value = "**<t:{}:{}>**".format(int(d2.timestamp()) , 'F') ,
                        inline = False)
        embed.add_field(name = "Erstellt am:" , value = "**<t:{}:{}>**".format(int(d1.timestamp()) , 'F') ,
                        inline = False)
        embed.set_footer(text = f"User-ID: {member.id}" , icon_url = member.avatar.url)
        embed.set_thumbnail(url = member.avatar.url)
        channel = await self.zeus.fetch_channel(904464407298457601)
        return await channel.send(embed = log_embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.bot:
            pass
        else:
            d1 = member.created_at
            d2 = member.joined_at
            embed = discord.Embed(color = discord.Colour.random() ,
                                  title = f"{member} hat {member.guild.name} verlassen")  # F-Strings!
            embed.add_field(name = "Beigetreten am:" , value = "**<t:{}:{}>**".format(int(d2.timestamp()) , 'F') ,
                            inline = False)
            embed.add_field(name = "Erstellt am:" , value = "**<t:{}:{}>**".format(int(d1.timestamp()) , 'F') ,
                            inline = False)
            embed.set_footer(text = f"User-ID: {member.id}" , icon_url = member.avatar.url)
            embed.set_thumbnail(url = member.avatar.url)
            channel = await self.zeus.fetch_channel(904464322556755980)
            return await channel.send(embed = embed)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        created = guild.created_at
        embed = discord.Embed(color = discord.Colour.random(),
                              title = f"Ich wurde zu {guild.name} eingeladen")
        embed.add_field(name="Inhaber:", value = guild.owner, inline = False)
        embed.add_field(name = "ID:", value = guild.owner_id, inline = False)
        embed.add_field(name="Erstellt am:", value = "**<t:{}:{}>**".format(int(created.timestamp()), 'F'), inline = False)
        embed.set_footer(text = f"Server-ID: {guild.id}")
        channel = await self.zeus.fetch_channel(904464360263548999)
        return await channel.send(embed=embed)

def setup(zeus):
    zeus.add_cog(message_logs(zeus))
