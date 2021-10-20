import aiohttp
import asyncio
import pysmartthings
token = '45ffbc3b-e055-427a-8e7e-3531a503fb82'

devices_name=["Led Strip","Lamp","Bedroom Lights","Main Light","Waterfall","Second Light","Tv","Moon","Second Light"]
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())



# async def switchON_OFF(deviceTarget,command):
#
#     try:
#
#
#                 except:
#                     pass



async def getDeviceList():
    async with aiohttp.ClientSession() as session:
        api = pysmartthings.SmartThings(session, token)
        devices =await api.devices()
        for i in devices:
            print(i.label)
            print(i.capabilities)


async def TvCommands(command,vol=None):
    async with aiohttp.ClientSession() as session:
        api = pysmartthings.SmartThings(session, token)
        devices =await api.devices()
        for i in devices:
            if i.label == "Tv":
                result = await i.command("main", "switch", "on")
                if command == "mute":
                    result = await i.mute(set_status=True)
                    assert result == True
                    print("mute successful")
                if command == "unmute":
                    result = await i.unmute(set_status=True)
                    assert result == True
                    print("unmute successful")
                if command == "volume":
                    result = await i.set_volume(vol,set_status=True)
                    assert result == True
                    print("volume set successful")

async def RGB_Commands(command,color = None,dimmer=None):
    async with aiohttp.ClientSession() as session:
        lista = [["rosu","verde","albastru","mov"],[0,30,70,80]]
        api = pysmartthings.SmartThings(session, token)
        devices = await api.devices()
        for device in devices:
            if device.label == "Led Strip":
                result = await device.command("main", "switch", "on")
                if command == "set color" and color in lista[0]:
                    cod=lista[1][lista[0].index(color)]
                    try:
                        result = await device.set_color(int(cod),100,set_status=True)     # 0=rosu ,30= verde ,70=albastru  ,80 =mov
                        assert result == True
                    except:
                        pass
                if command == "set dimmer":
                    result = await device.set_level(int(dimmer))  # 0=rosu ,30= verde ,70=albastru  ,80 =mov
                    assert result == True


# def convertSwitch(deviceTarget,command):
#     try:
#         asyncio.run(switchON_OFF(deviceTarget,command))
#     except Exception as o:
#         print(o)


# convertSwitch("Moon","off")