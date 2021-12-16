import aiohttp


async def get_anime(url: str):
    params = dict()
    params['url'] = url
    async with aiohttp.ClientSession() as session:
        async with session.get('https://trace.moe/api/search', params=params) as res:
            anime_json = await res.json(content_type=None)
    repass = ""
    for anime in anime_json["docs"][:3]:
        anime_name = anime["anime"]
        episode = anime["episode"]
        at = int(anime["at"])
        m, s = divmod(at, 60)
        similarity = anime["similarity"]

        putline = "[ {} ][{}][{}:{}] 相似度:{:.2%}".format(anime_name, episode if episode else '?', m, s, similarity)
        if repass:
            repass = "\n".join([repass, putline])
        else:
            repass = putline

    return repass
