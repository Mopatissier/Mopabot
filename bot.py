import discord
import datetime
import pytz
import re
import asyncio
import os

from datetime import datetime, date
from discord.ext.commands import Bot

if os.path.exists("config.py"):
    import config

BOT_PREFIX = "!"

is_online = os.environ.get('IS_HEROKU', None)
if is_online:
    TOKEN = str(os.environ.get('TOKEN', None))
else:
    TOKEN = config.TOKEN

her_id = "220042310526697473" #Whispie
# her_id = "163256075745755136" #Sayushii
# her_id = "139479225655623680" #Adri
id_me = "332213498513981441" #Moi

client = Bot(command_prefix=BOT_PREFIX)

confirmation_late = 0
test_working = False


@client.command(description="Record what you say, and give the message later. Use it like this: !message 14h03.",
                brief="Record a message.",
                pass_context=True)
async def message(ctx):
    tz = pytz.timezone('US/Eastern')

    her = await client.get_user_info(her_id)

    if ctx.message.author.id == her_id:
        await client.say("Hehe, well tried, Whispie, but I'm only allowed to obey Mopati. :3")
        await client.say("If you want me to allow you something, ask my creator for it!")
        return

    if ctx.message.author.id != id_me:
        await client.say("Well tried, but only Mopati can use Mopabot!")
        return

    timestring = ctx.message.content

    if len(timestring) < 14:
        await client.say("Time must be written like 04h09!")
        return

    extract = timestring[9:14]

    if not (extract[0:1].isdigit()) or not (extract[2] == "h") or not (extract[3:4].isdigit()):
        await client.say("You didn't write the time properly!")
        return

    extract = re.findall('\d+', extract)
    hour = int(extract[0])
    minute = int(extract[1])

    if hour >= 24 or minute >= 60:
        await client.say("I need a valid time!")
        return

    await client.say("Recording...")

    time = {}
    msg = {}
    i = 0
    msg[0] = '  '

    while msg[i] != 'stop':
        messagerecord = await client.wait_for_message()
        if messagerecord.content != "Recording...":
            i = i + 1
            msg[i] = messagerecord.content
            time[i] = datetime.now(tz).time()

    await client.say("End of recording.")

    timewait = datetime(2000, 1, 1, hour, minute, 0)
    realtime = datetime.now(tz).time()

    while realtime.second is not 0:
        await asyncio.sleep(1)
        realtime = datetime.now(tz).time()

    while timewait.hour is not realtime.hour or timewait.minute is not realtime.minute:
        await asyncio.sleep(60)
        realtime = datetime.now(tz).time()

    i2 = 1
    while i2 < i:

        if i2 != 1:
            decalage = datetime.combine(date.min, time[i2]) - datetime.combine(date.min, time[i2 - 1])

            await asyncio.sleep(decalage.seconds)

        await client.send_message(her, msg[i2])

        i2 = i2 + 1

    await client.say("Message sent!")


@client.command(description="Record a message, and give it if Whispie sleeps late.",
                brief="Say a message when she's awake late.",
                pass_context=True)
async def late(ctx):
    global confirmation_late

    tz = pytz.timezone('US/Eastern')

    if ctx.message.author.id == her_id:
        await client.say("Hehe, well tried, Whispie, but I'm only allowed to obey Mopati. :3")
        await client.say("If you want me to allow you something, ask my creator for it!")
        return

    if ctx.message.author.id != id_me:
        await client.say("Well tried, but only Mopati can use Mopabot!")
        return

    if ctx.message.server is None:
        await client.say("You have to use this command in a server!")
        return

    her = ctx.message.author.server.get_member(her_id)

    if confirmation_late == 0:
        confirmation_late = 1
    else:
        await client.say("The message is still up, don't worry about that.")
        return

    await client.say("Recording...")

    time = {}
    msg = {}
    i = 0
    msg[0] = '  '

    while msg[i] != 'stop':
        messagerecord = await client.wait_for_message()
        if messagerecord.content != "Recording...":
            i = i + 1
            msg[i] = messagerecord.content
            time[i] = datetime.now(tz).time()

    await client.say("End of recording.")

    timemax = datetime(2000, 1, 1, 4, 0, 0)
    timemin = datetime(2000, 1, 1, 1, 0, 0)
    realtime = datetime.now(tz).time()

    awake = 0
    while awake == 0:
        if timemin.hour <= realtime.hour < timemax.hour and str(her.status) == 'online':
            awake = 1
        else:
            await asyncio.sleep(1)
            realtime = datetime.now(tz).time()

    i2 = 1
    while i2 < i:

        if i2 != 1:
            decalage = datetime.combine(date.min, time[i2]) - datetime.combine(date.min, time[i2 - 1])

            await asyncio.sleep(decalage.seconds)

        await client.send_message(her, msg[i2])

        i2 = i2 + 1

    await client.say("Whispie went sleeping late!")
    confirmation_late = 0


@client.command()
async def test():
    global test_working

    if test_working is False:
        test_working = True
        await client.say("Test mode : on.")
    else:
        test_working = False
        await client.say("Test mode : off.")

    while test_working:
        await client.say("I'm still working.")
        await asyncio.sleep(60*15)


client.run(TOKEN)
