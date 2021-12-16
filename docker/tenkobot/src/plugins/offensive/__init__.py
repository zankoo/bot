import aiohttp
import json
from nonebot import on_message
from nonebot.adapters.cqhttp import Bot, Event, Message, MessageSegment, escape
from nonebot.rule import to_me
from nonebot.typing import T_State


async def get_access_token():
    params = dict()
    params['grant_type'] = 'client_credentials'
    params['client_id'] = '8VTvksBwhkShQTL2xF361vVD'
    params['client_secret'] = 'SXhK4CwHeLlElgi3lU1TkgW26jY8DZ5R'
    async with aiohttp.ClientSession() as session:
        async with session.post('https://aip.baidubce.com/oauth/2.0/token', params=params) as res:
            json_data = await res.json()
            return json_data['access_token']


async def get_offensive_level(sentence_got: str):
    params = dict()
    params['text'] = sentence_got
    params['access_token'] = await get_access_token()
    headers = dict()
    headers['content-type'] = 'application/x-www-form-urlencoded'
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post('https://aip.baidubce.com/rest/2.0/solution/v1/text_censor/v2/user_defined',
                                    params=params,
                                    headers=headers) as res:
                json_data = json.loads(await res.text())
                return json_data['conclusion'] == '不合规'
    except Exception:
        return 0


async def get_offensive_word():
    headers = dict()
    headers['referer'] = 'https://zuanbot.com/'
    async with aiohttp.ClientSession() as session:
        async with session.get('https://zuanbot.com/api.php?lang=zh_cn', headers=headers) as res:
            return await res.text()


offensive = on_message(priority=2, block=True, rule=to_me())


@offensive.handle()
async def get_msg(bot: Bot, event: Event, state: T_State):
    if await get_offensive_level(str(event.get_message()).strip()):
        await offensive.finish(await get_offensive_word())
