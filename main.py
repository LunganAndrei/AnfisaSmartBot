import os
import discord
from discord.ext import commands, tasks
from discord_components import DiscordComponents, Button

from SeleniumModules import infoScrape as scrape
from SeleniumModules import shopPrices as pricescrape
from SeleniumModules import bookingScrape
from OpenCVModules import computerVision as handDetection
from OpenCVModules import handTrackingModule as htm
from DiscordModules import ListenCog
from DiscordModules import modules
from DeviceControl import CogModuleSmartDevices as SmartDevices
from DeviceControl import smartthingsModule


admins = [677998815764152321]

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


# ---------------------------------Event Functions---------------------------------------


bot.add_cog(ListenCog.ListenModules(bot))
bot.add_cog(SmartDevices.SmartDevicesClass(bot))
@bot.event
async def on_ready():
    DiscordComponents(bot)

    print('Main File ONLINE')


@bot.event
async def on_member_join(member):
    guild = bot.get_guild(853405938630524938)
    help_function = discord.Embed(
        title=f"Hello to the {guild.name} server,If you need some help with commands just say i need help", )
    await member.send(help_function)

# -------------------------------------Command Functions------------------------------
@bot.command(pass_context=True)
async def purge(ctx, amount=30):
    channel = ctx.message.channel
    messages = []
    async for message in channel.history(limit=amount + 1):
              messages.append(message)

    await channel.delete_messages(messages)


@commands.has_permissions(kick_members=True)
@bot.command()
async def kick(ctx, user: discord.Member, *, reason="No reason provided"):
    if user.name != "Lungan Andrei" and ctx.author.id in admins:
        await user.kick(reason=reason)
        kick = discord.Embed(title=f":boot: Kicked {user.name}!",
                             description=f"Reason: {reason}\nBy: {ctx.author.mention}")
        await ctx.message.delete()
        await ctx.channel.send(embed=kick)

    else:
        await ctx.channel.send("Nu esti autorizat sa folosesti comanda")



@bot.event
async def on_message(message: discord.Message):
    message_channel = bot.get_channel(891123316176343060)
    filename = ""
    image_types = ["png", "jpeg", "gif", "jpg"]
    for attachment in message.attachments:
        if any(attachment.filename.lower().endswith(image) for image in image_types):
            filename = attachment.filename
            await attachment.save(attachment.filename)
            fingers = handDetection.countFingers(attachment.filename)
            # print(fingers)
            await message_channel.send(f"{fingers} finger/s detected ")
    try:
        os.remove(filename)
    except:
        pass

bot.run(os.environ["token"])
