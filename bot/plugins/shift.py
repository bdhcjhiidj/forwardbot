from . import *


@bot.on(events.NewMessage(incoming=True, pattern="/shift (.*)"))
async def _(e):
    if not (is_auth(e.sender_id)):
        return 
    x = e.pattern_match.group(1)
    z = await e.reply("`processing..`")
    a, b = x.split("|")
    try:
        c = int(a)
    except Exception:
        try:
            c = (await bot.get_entity(a)).id
        except Exception:
            await z.edit("invalid Channel given")
            return
    try:
        d = int(b)
    except Exception:
        try:
            d = (await bot.get_entity(b)).id
        except Exception:
            await z.edit("invalid Channel given")
            return
    async for msg in user.iter_messages(int(c), reverse=True):
        try:
            await asyncio.sleep(0.5)
            m = await bot.get_messages(int(c), ids=msg.id)
            await bot.send_message(int(d), m)
        except BaseException:
            pass
    await z.edit("Done")
