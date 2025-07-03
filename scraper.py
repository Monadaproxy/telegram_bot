from bs4 import BeautifulSoup
from fetchers import fetch_anilist, fetch_html
import random
ANILIST_URL = "https://graphql.anilist.co"
ANIMEGO_URL = "https://animego.org"

async def get_random_anime() -> str:
    random_offset = random.randint(0, 100)

    query = """
    query {
        Page(perPage: 1) {
            media(type: ANIME, sort: ID_DESC) {
                title { 
                    romaji
                }
                description(asHtml: false)
                siteUrl
            }
        }
    }
    """
    variables = {'offset': random_offset}
    data = await fetch_anilist(ANILIST_URL, query, variables)

    if not data["data"]:
        return f"Не удалось найти аниме 😢 Попробуйте ещё раз! {data}"

    media = data["data"]["Page"]["media"][0]
    return f"{media['title']['romaji']}\n\n{media['description']}"

async def get_top_10() -> str:
    query = """
    query {
        Page(perPage: 10) {
            media(type: ANIME, sort: SCORE_DESC) {
                title {  
                    romaji
                }
                startDate { year }
            }
        }
    }
    """
    data = await fetch_anilist(ANILIST_URL, query, {})
    top = data["data"]["Page"]["media"]
    return "\n".join(
        f'{i+1}. "{item["title"]["romaji"]}" ({item["startDate"]["year"]})'
        for i, item in enumerate(top)
    )

async def get_new_episodes() -> str:
    html = await fetch_html(ANIMEGO_URL)
    soup = BeautifulSoup(html, "html.parser")
    episodes = soup.select(".last-updates .episode-item")[:10]
    return "\n".join(ep.text.strip() for ep in episodes)