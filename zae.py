import asyncio
import sys
import time
import traceback
import os
import datetime
from datetime import datetime
import discord
from discord.ext import commands

intents = discord.Intents().all()

zeus = commands.Bot(
    command_prefix = {"<@901585159848095765>" , "<@!901585159848095765>" , "zae!" , "zAe!" , "ZaE!" , "ZAE!" , "Zae!" ,
                      "zAE!"} , case_insensitive = True , intents = intents)

zeus.remove_command("help")

startTime = time.time()


@zeus.event
async def statuschange():
    await zeus.wait_until_ready()
    while True:
        servers = len(zeus.guilds)
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

        await zeus.change_presence(
            activity = discord.Activity(type = discord.ActivityType.competing, name = f"{servers} Servern mit {members} Usern")
        )
        await asyncio.sleep(60)


initial_extensions = [
    'zeus.mod',
    'zeus.music',
    'zeus.infos',
    'zeus.devcmds',
    'zeus.error-handler',
    'zeus.botinfos',
    'zeus.help-cmd'
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


zeus.run(os.getenv("token") , reconnect = True)
