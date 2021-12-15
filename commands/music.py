import asyncio
import discord
import youtube_dl
from discord.ext import commands

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class music(commands.Cog):
    def __init__(self, zeus):
        self.zeus = zeus

    @commands.command(description="joins a voice channel")
    async def join(self, ctx):
        if ctx.author.voice is None or ctx.author.voice.channel is None:
            return await ctx.send('Du musst in einem Voice-Chat sein!')

        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            vc = await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)
            vc = ctx.voice_client

    @commands.command(description="Streamt Music")
    async def play(self, ctx, *, url):
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.zeus.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print('Fehler aufgetreten!: %s' % e) if e else None)
        embed = discord.Embed(timestamp = ctx.message.created_at, color = discord.Colour.random(), title="Musik wird abgespielt!")
        embed.set_author(name = f"{ctx.author}", icon_url = ctx.author.display_avatar)
        embed.add_field(name = "URL:", value = f"{url}", inline = False)
        embed.add_field(name = "Name:", value = f"{player.title}", inline = False)
        embed.add_field(name = "Angefordert von:", value = f"{ctx.author}", inline = False)
        embed.set_footer(text = f"User-ID: {ctx.author.id}", icon_url = ctx.author.display_avatar)
        await ctx.reply(embed=embed, mention_author = False)
    
    @commands.command(description="pauses music")
    async def pause(self, ctx):
        ctx.voice_client.pause()
    
    @commands.command(description="resumes music")
    async def resume(self, ctx):
        ctx.voice_client.resume()

    @commands.command(description="stops and disconnects the bot from voice")
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()

    @play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

def setup(zeus):
    zeus.add_cog(music(zeus))
