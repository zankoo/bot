import random
from bilibili_api import user, video
from nonebot import on_command, on_message, on_keyword, require, on_notice
from nonebot.adapters.cqhttp import Bot, Event, Message, MessageSegment, escape
from nonebot.rule import to_me
from nonebot.typing import T_State
import time
import aiohttp
import nonebot

image = on_command("st", aliases={"搜图"}, priority=1, block=True)


async def search(url: str):
    params = dict()
    params['api_key'] = 'bd30999b55a3b42b6414d2357061d92b1bf2daa5'
    params['output_type'] = 2
    params['testmode'] = 0
    params['db'] = 999
    params['numres'] = 3
    params['url'] = url
    async with aiohttp.ClientSession() as session:
        async with session.get('https://saucenao.com/search.php', params=params) as res:
            return await res.json()


async def get_view(url: str) -> str:
    sauces = await search(url)
    repass = ""
    try:
        for sauce in sauces['results']:
            url = sauce['data']['ext_urls'][0].replace("\\", "").strip()
            similarity = sauce['header']['similarity']
            putline = "[{}] 相似度:{}%".format(url, similarity)
            if repass:
                repass = "\n".join([repass, putline])
            else:
                repass = putline
    except Exception as e:
        repass = "没有结果"

    return repass


@image.handle()
async def image_search(bot: Bot, event: Event, state: T_State):
    args = ''
    try:
        args = event.get_message().pop()['data']['url']
    except Exception:
        pass
    if args != '':
        state['image'] = args


async def parser(bot: Bot, event: Event, state: T_State):
    state[state["_current_key"]] = event.get_message().pop()['data']['url']


@image.got('image', prompt='请发送图片', args_parser=parser)
async def handle_image(bot: Bot, event: Event, state: T_State):
    await image.finish(await get_view(state['image']))

# @weather.handle()
# async def handle_first_receive(bot: Bot, event: Event, state: T_State):
#     args = str(event.get_message()).strip()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
#     if args:
#         state["city"] = args  # 如果用户发送了参数则直接赋值
#
#
# @weather.got("city", prompt="你想查询哪个城市的天气呢？")
# async def handle_city(bot: Bot, event: Event, state: T_State):
#     city = state["city"]
#     if city not in ["上海", "北京"]:
#         await weather.reject("你想查询的城市暂不支持，请重新输入！")
#     city_weather = await get_weather(city)
#     await weather.finish(city_weather)
