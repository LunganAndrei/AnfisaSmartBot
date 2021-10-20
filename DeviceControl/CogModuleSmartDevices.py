# import aiohttp
import asyncio
# import discord
# import asyncpg
# import pysmartthings
import os

import aiohttp
import asyncpg
import pysmartthings
from discord_components import DiscordComponents, Button
from discord.ext import commands,tasks

# from DeviceControl import smartthingsModule as smartModule

token = os.environ["smartthings_token"]
devices_name=["Led Strip","Lamp","Bedroom Lights","Main Light","Waterfall","Second Light","Tv","Moon","Second Light"]
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class SmartDevicesClass(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._last_member = None


    @commands.Cog.listener()
    async def on_ready(self):
        DiscordComponents(self.bot)
        print('SmartDeviceController ONLINE')


    @commands.Cog.listener()
    async def on_message(self, ctx):
        cmdList = ["turn on", "turn off"]
        if any(word in ctx.content.lower() for word in cmdList) and ctx.author.id == 677998815764152321:
            answer_list=ctx.content.split()
            answer_list.pop(0)
            async with aiohttp.ClientSession() as session:
                api = pysmartthings.SmartThings(session, token)
                devices = await api.devices()
                for device in devices:
                    if device.label == answer_list[1] and answer_list[1] in devices_name:

                        try:
                            result = await device.command("main", "switch", answer_list[0])
                            assert result == True
                            await ctx.channel.send(f"The device {answer_list[1]} turned {answer_list[0]} successfully")
                            # return True
                        except:
                            await ctx.channel.send("something happened, please check the device name")

