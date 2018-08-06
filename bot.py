import discord
import datetime
import pytz
import re
import asyncio

from datetime import datetime, date
from discord.ext.commands import Bot

import configtest

BOT_PREFIX = "!"
TOKEN = config.token_secret

her_id = "220042310526697473" #Whispie
# her_id = "163256075745755136" #Sayushii
# her_id = "139479225655623680" #Adri
id_me = "332213498513981441" #Moi

client = Bot(command_prefix=BOT_PREFIX)


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


client.run(TOKEN)
