from fetchers import fetch_anilist
import random
import re

ANILIST_URL = "https://graphql.anilist.co"
ANIMEGO_URL = "https://animego.org"

def clean_html(raw_html):
    clean_text = re.sub(r'<[^>]+>', '', raw_html)
    clean_text = clean_text.replace('&quot;', '"')
    clean_text = clean_text.replace('&amp;', '&')
    return clean_text.strip()


async def get_random_anime() -> dict:
    try:
        random_offset = random.randint(1, 10000)

        query = """
        query ($page: Int) {
            Page(page: $page, perPage: 1) {
                media(type: ANIME, sort: ID, isAdult: false) {
                    title { romaji }
                    description
                    siteUrl
                    coverImage {
                        large
                    }
                }
            }
        }
        """
        variables = {"page": random_offset}

        data = await fetch_anilist(ANILIST_URL, query, variables)
        media = data["data"]["Page"]["media"]

        if not media:
            return "Не удалось найти аниме 😢 Попробуйте ещё раз!"

        item = media[0]
        title = item["title"]["romaji"]
        desc = (item["description"] or "Описание отсутствует")
        clean_desc = clean_html(desc)[:1000]
        cover_url = item["coverImage"]["large"] if item["coverImage"] else None

        return {
            "title": title,
            "description": clean_desc,
            "cover_url": cover_url,
            "url": item["siteUrl"]
        }

    except Exception as e:
        return {"error": e}

async def get_top_10() -> str:
    query = """
    query {
        Page(perPage: 10) {
            media(type: ANIME, sort: SCORE_DESC) {
                title { romaji }
                startDate { year }
            }
        }
    }
    """
    data = await fetch_anilist(ANILIST_URL, query, {})
    top = data["data"]["Page"]["media"]
    return "🏆 <b>Топ 10 аниме по версии Anilist:</b>\n" + "\n".join(
        f'{i+1}. "{item["title"]["romaji"]}" ({item["startDate"]["year"]})'
        for i, item in enumerate(top)
    )


async def get_new_episodes() -> str:
    query = """
    query {
        Page(perPage: 10) {
            media(type: ANIME, sort: UPDATED_AT_DESC) {
                title { romaji }
                episodes
                siteUrl
            }
        }
    }
    """
    data = await fetch_anilist(ANILIST_URL, query, {})
    episodes = []
    for item in data["data"]["Page"]["media"]:
        title = item["title"]["romaji"]
        episodes.append(f"• {title} - {item['episodes'] or '?'} серия")
    return "📢 <b>Последние вышедшие серии:</b>\n" + "\n".join(episodes)