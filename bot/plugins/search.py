# Ported From https://github.com/kaif-00z/ForwarderBot
# (c) @kaif-00z for @TeamUltroid

"""
`/search <channel/group id> <query>` Will send all the related file/message/media from id
"""


import re

from . import *

asst = bot
ultroid_bot = user

X = []
Z = []


@bot.on(
    events.NewMessage(
        incoming=True, pattern="\\/search ?(.*)", func=lambda x: not x.is_group
    )
)
async def src(event):
    query = event.pattern_match.group(1)
    btn = [Button.inline("CANCEL PROCESS", data="cnc")]
    x = await event.reply("`searching...`", buttons=btn)
    async for message in ultroid_bot.iter_messages(
        Var.GROUP_ID, search=query, reverse=True
    ):
        if message:
            if event.sender_id not in X:
                X.append(event.sender_id)
            msg = await asst.get_messages(udB.get_key("DUMP_CHANNEL"), ids=message.id)
            await asst.send_message(event.chat_id, msg)
            if event.sender_id in Z:
                Z.remove(event.sender_id)
                return await x.delete()
            await asyncio.sleep(1)
            continue
    if event.sender_id not in X:
        await asst.send_message(
            event.chat_id,
            f"**Nothing Found Related To Keyword :** `{query}`\nFor More Info - @Anime_Chat_Ocean",
        )
    else:
        await asst.send_message(
            event.chat_id,
            f"All Files Related To Keyword : `{query}` sent successfully.\nFor More Info - @Anime_chat_ocean",
        )
        X.remove(event.sender_id)
    await x.delete()


@bot.on(events.callbackquery.CallbackQuery(data=re.compile("cnc")))
async def _(e):
    Z.append(e.sender_id)
