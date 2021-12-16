from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, Event, Message, MessageSegment, escape
from nonebot.typing import T_State
from .data_source import get_anime

anime = on_command("sf", aliases={"搜番"}, priority=1, block=True)


@anime.handle()
async def anime_search(bot: Bot, event: Event, state: T_State):
    args = ''
    try:
        args = event.get_message().pop()['data']['url']
    except Exception:
        pass
    if args != '':
        state['image'] = args


async def parser(bot: Bot, event: Event, state: T_State):
    state[state["_current_key"]] = event.get_message().pop()['data']['url']


@anime.got('image', prompt='请发送图片', args_parser=parser)
async def handle_image(bot: Bot, event: Event, state: T_State):
    await anime.finish(await get_anime(state['image']))

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
#
