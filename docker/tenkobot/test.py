import aiohttp
import asyncio
import time
import json


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
    async with aiohttp.ClientSession() as session:
        async with session.post('https://aip.baidubce.com/rest/2.0/solution/v1/text_censor/v2/user_defined',
                                params=params,
                                headers=headers) as res:
            json_data = json.loads(await res.text())
            print(json_data['conclusion'])


async def get_offensive_word():
    headers = dict()
    headers['referer'] = 'https://zuanbot.com/'
    async with aiohttp.ClientSession() as session:
        async with session.get('https://zuanbot.com/api.php?lang=zh_cn', headers=headers) as res:
            print(await res.text())


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    task = loop.create_task(get_offensive_word())
    loop.run_until_complete(task)
