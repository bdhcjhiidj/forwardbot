# ported from catuserbot
# modified by @kaif-00z

import textwrap

import requests
from html_telegraph_poster import TelegraphPoster
import jikanpy
from jikanpy import Jikan
from pySmartDL import SmartDL

from . import *

jikan = Jikan()


async def post_to_telegraph(page_title, html_format_content):
    post_client = TelegraphPoster(use_api=True)
    auth_name = "ForwarderBot"
    post_client.create_api_token(auth_name)
    post_page = post_client.post(
        title=page_title,
        author=auth_name,
        author_url="https://t.me/anime_ocean",
        text=html_format_content,
    )
    return post_page["url"]


def getPosterLink(mal):
    # grab poster from kitsu
    kitsu = getKitsu(mal)
    image = requests.get(f"https://kitsu.io/api/edge/anime/{kitsu}").json()
    return image["data"]["attributes"]["posterImage"]["original"]


def getKitsu(mal):
    # get kitsu id from mal id
    link = f"https://kitsu.io/api/edge/mappings?filter[external_site]=myanimelist/anime&filter[external_id]={mal}"
    result = requests.get(link).json()["data"][0]["id"]
    link = f"https://kitsu.io/api/edge/mappings/{result}/item?fields[anime]=slug"
    return requests.get(link).json()["data"]["id"]


def getBannerLink(mal, kitsu_search=True, anilistid=0):
    # try getting kitsu backdrop
    if kitsu_search:
        kitsu = getKitsu(mal)
        image = f"http://media.kitsu.io/anime/cover_images/{kitsu}/original.jpg"
        response = requests.get(image)
        if response.status_code == 200:
            return image
    if anilistid != 0:
        return f"https://img.anili.st/media/{anilistid}"
    # try getting anilist banner
    query = """
    query ($idMal: Int){
        Media(idMal: $idMal){
            bannerImage
        }
    }
    """
    data = {"query": query, "variables": {"idMal": int(mal)}}
    image = requests.post("https://graphql.anilist.co", json=data).json()["data"][
        "Media"
    ]["bannerImage"]
    if image:
        return image
    return getPosterLink(mal)


async def get_anime_manga(mal_id, search_type, _user_id):  # sourcery no-metrics
    jikan = jikanpy.jikan.Jikan()
    if search_type == "anime_anime":
        result = jikan.anime(mal_id)
        trailer = result["trailer_url"]
        if trailer:
            TRAILER = f"<a href='{trailer}'>🎬 Trailer</a>"
        else:
            TRAILER = "🎬 <i>No Trailer Available</i>"
        studio_string = ", ".join(
            studio_info["name"] for studio_info in result["studios"]
        )
        producer_string = ", ".join(
            producer_info["name"] for producer_info in result["producers"]
        )
    elif search_type == "anime_manga":
        result = jikan.manga(mal_id)
        image = result["image_url"]
    caption = f"📺 <a href='{result['url']}'>{result['title']}</a>"
    if result["title_japanese"]:
        caption += f" ({result['title_japanese']})\n"
    else:
        caption += "\n"
    alternative_names = []
    if result["title_english"] is not None:
        alternative_names.append(result["title_english"])
    alternative_names.extend(result["title_synonyms"])
    if alternative_names:
        alternative_names_string = ", ".join(alternative_names)
        caption += f"\n<b>Also known as</b>: <i>{alternative_names_string}</i>"
    genre_string = ", ".join(genre_info["name"] for genre_info in result["genres"])
    if result["synopsis"] is not None:
        synopsis = result["synopsis"].split(" ", 60)
        try:
            synopsis.pop(60)
        except IndexError:
            pass
        synopsis_string = " ".join(synopsis) + "..."
    else:
        synopsis_string = "Unknown"
    for entity in result:
        if result[entity] is None:
            result[entity] = "Unknown"
    if search_type == "anime_anime":
        anime_malid = result["mal_id"]
        anime_result = await anime_json_synomsis(
            anime_query, {"idMal": anime_malid, "asHtml": True, "type": "ANIME"}
        )
        anime_data = anime_result["data"]["Media"]
        html_char = ""
        for character in anime_data["characters"]["nodes"]:
            html_ = ""
            html_ += "<br>"
            html_ += f"""<a href="{character['siteUrl']}">"""
            html_ += f"""<img src="{character['image']['large']}"/></a>"""
            html_ += "<br>"
            html_ += f"<h3>{character['name']['full']}</h3>"
            html_ += f"<em>{character['name']['native']}</em><br>"
            html_ += f"<b>Character ID</b>: {character['id']}<br>"
            html_ += f"<h4>About Character and Role:</h4>{character.get('description', 'N/A')}"
            html_char += f"{html_}<br><br>"
        studios = "".join(
            "<a href='{}'>• {}</a> ".format(studio["siteUrl"], studio["name"])
            for studio in anime_data["studios"]["nodes"]
        )
        coverImg = anime_data.get("coverImage")["extraLarge"]
        bannerImg = anime_data.get("bannerImage")
        anilist_animelink = anime_data.get("siteUrl")
        title_img = coverImg or bannerImg
        romaji = anime_data["title"]["romaji"]
        native = anime_data["title"]["native"]
        english = anime_data["title"]["english"]
        image = getBannerLink(mal_id, False, anime_data.get("id"))
        # Telegraph Post mejik
        html_pc = ""
        html_pc += f"<h1>{native}</h1>"
        html_pc += "<h3>Synopsis:</h3>"
        html_pc += result["synopsis"] or "Unknown"
        html_pc += "<br>"
        if html_char:
            html_pc += "<h2>Main Characters:</h2>"
            html_pc += html_char
            html_pc += "<br><br>"
        html_pc += "<h3>More Info:</h3>"
        html_pc += f"<br><b>Studios:</b> {studios}<br>"
        html_pc += (
            f"<a href='https://myanimelist.net/anime/{anime_malid}'>View on MAL</a>"
        )
        html_pc += f"<a href='{anilist_animelink}'> View on anilist.co</a>"
        html_pc += f"<img src='{bannerImg}'/>"
        title_h = english or romaji
    if search_type == "anime_anime":
        caption += textwrap.dedent(
            f"""
        🆎 <b>Type</b>: <i>{result['type']}</i>
        🆔 <b>MAL ID</b>: <i>{result['mal_id']}</i>
        📡 <b>Status</b>: <i>{result['status']}</i>
        🎙️ <b>Aired</b>: <i>{result['aired']['string']}</i>
        🔢 <b>Episodes</b>: <i>{result['episodes']}</i>
        🔞 <b>Rating</b>: <i>{result['rating']}</i>
        💯 <b>Score</b>: <i>{result['score']}</i>
        🌐 <b>Premiered</b>: <i>{result['premiered']}</i>
        ⌛ <b>Duration</b>: <i>{result['duration']}</i>
        🎭 <b>Genres</b>: <i>{genre_string}</i>
        🎙️ <b>Studios</b>: <i>{studio_string}</i>
        💸 <b>Producers</b>: <i>{producer_string}</i>
        """
        )
        synopsis_link = await post_to_telegraph(
            title_h,
            f"<img src='{title_img}' title={romaji}/>\n"
            + f"<code>{caption}</code>\n"
            + f"{TRAILER}\n"
            + html_pc,
        )
        caption += f"<b>{TRAILER}</b>\n📖 <a href='{synopsis_link}'><b>Synopsis</b></a> <b>&</b> <a href='{result['url']}'><b>Read More</b></a>"
    elif search_type == "anime_manga":
        caption += textwrap.dedent(
            f"""
        🆎 <b>Type</b>: <i>{result['type']}</i>
        📡 <b>Status</b>: <i>{result['status']}</i>
        🔢 <b>Volumes</b>: <i>{result['volumes']}</i>
        📃 <b>Chapters</b>: <i>{result['chapters']}</i>
        📊 <b>Rank</b>: <i>{result['rank']}</i>
        💯 <b>Score</b>: <i>{result['score']}</i>
        🎭 <b>Genres</b>: <i>{genre_string}</i>
        📖 <b>Synopsis</b>: <i>{synopsis_string}</i>
        """
        )
    return caption, image


@bot.on(events.NewMessage(incoming=True, pattern="\\/anime"))
async def get_anime(event):
    input_str = event.text.split(" ", maxsplit=1)[1]
    reply = await event.get_reply_message()
    if not input_str:
        if reply:
            input_str = reply.text
        else:
            return await event.reply(
                "What should i search ? Gib me Something to Search"
            )
    x = await event.reply("Searching Anime..")
    jikan = jikanpy.jikan.Jikan()
    search_result = jikan.search("anime", input_str)
    first_mal_id = search_result["results"][0]["mal_id"]
    caption, image = await get_anime_manga(first_mal_id, "anime_anime", event.chat_id)
    try:
        downloader = SmartDL(image, anime_path, progress_bar=False)
        downloader.start(blocking=False)
        while not downloader.isFinished():
            pass
        await event.client.send_file(
            event.chat_id,
            file=anime_path,
            caption=caption,
            parse_mode="HTML",
        )
        await x.delete()
        os.remove(anime_path)
    except BaseException:
        image = getBannerLink(first_mal_id, True)
        await event.client.send_file(
            event.chat_id,
            file=image,
            caption=caption,
            parse_mode="HTML",
        )
