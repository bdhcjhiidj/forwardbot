from requests.utils import requote_uri

from . import *

BASE_URL = "https://tg.animeocean.workers.dev/0:search?q={}"

@bot.on(events.NewMessage(incoming=True, pattern="\\/index ?(.*)"))
async def indexx(e):
    query = e.pattern_match.group(1)
    msg = requote_uri(BASE_URL.format(query))
    await e.reply(f"Get it here - [link]({msg})")
