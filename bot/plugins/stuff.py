#    This file is part of the Forwarder distribution.
#    Copyright (c) 2022 kaif-00z
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 3.
#
#    This program is distributed in the hope that it will be useful, but
#    WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#    General Public License for more details.
#
# License can be found in
# <https://github.com/kaif-00z/ForwarderBot/blob/main/License> .


from . import *


@bot.on(events.NewMessage(incoming=True, pattern="\\/ping"))
async def _(event):
    t = time.time()
    now = dt.now()
    x = await event.reply("`Pɪɴɢ!!!`")
    tt = time.time() - t
    v = ts(int((now - uptime).seconds) * 1000)
    p = float(str(tt)) * 1000
    await x.edit(f"**Uptime**: {v}\n**Pɪɴɢ !!**: {int(p)}ms")


@bot.on(events.NewMessage(incoming=True, pattern="\\/start"))
async def strt(event):
    await event.reply(
        f"Hi `{event.sender.first_name}` \nHi I am Official Bot of Anime Ocean",
        buttons=[
            [
                Button.inline("Info", data="inf"),
            ],
        ],
    )


@bot.on(events.callbackquery.CallbackQuery(data=re.compile("inf")))
async def _(e):
    await e.edit(f"**Powered By @BotzCenter**")
