import random
from bilibili_api import user, video
from nonebot import on_command, on_message, on_keyword, require, on_notice
from nonebot.adapters.cqhttp import Bot, Event, Message, MessageSegment, escape
from nonebot.rule import to_me
from nonebot.typing import T_State
import time
import aiohttp
import nonebot


async def get_yellow_date_new():
    data = {'date': time.strftime("%Y-%-m-%-d", time.localtime()), 'key': '52d12ebe7ee2658cddccfc8d0fad4e1a'}
    url = 'http://v.juhe.cn/calendar/day'
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=data) as res:
            return await res.json()


async def process(content: str):
    contents = content.split('.')
    result = ''
    for idx, item in enumerate(contents):
        result += item + '.'
        if (idx + 1) % 4 == 0:
            result += '\n\t'
    return result


yellow_date = on_command("hl", aliases={"黄历"}, priority=1, block=True)


@yellow_date.handle()
async def yellow_date_handle(bot: Bot, event: Event, state: T_State):
    date = await get_yellow_date_new()
    good = await process(date['result']['data']['suit'])
    bad = await process(date['result']['data']['avoid'])
    year = date['result']['data']['lunarYear'][0:2] + date['result']['data']['animalsYear'] + "年" + \
           date['result']['data']['lunar']
    if date['reason'] == 'Success':
        result = (f"今：{year}\n"
                  f"宜：{good}\n"
                  f"忌：{bad}")
    else:
        result = "今日查询次数已用完"
    await yellow_date.finish(result)
