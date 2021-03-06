from . import *

INLOCK = "`Seems like inline messages aren't allowed here`"


@bot.on(events.NewMessage(incoming=True, pattern="/manga"))
async def _(e):
    keyword = ""
    msg = await e.reply("`Searching ...`")
    try:
        keyword = e.text.split(" ", maxsplit=1)[1]
    except BaseException:
        pass
    if not keyword:
        return await msg.edit("`Provide a Keyword to search`")
    try:
        animes = await user.inline_query("animedb_bot", f"<m> {keyword}")
        ok = await animes[0].click(
            Var.LOG_CHANNEL,
            reply_to=e.reply_to_msg_id,
            silent=True if e.is_reply else False,
            hide_via=True,
        )
        await bot.send_message(e.chat_id, ok)
        await msg.delete()
        await ok.delete()
        return
    except Exception:
        return await msg.edit("`No Results Found`")
