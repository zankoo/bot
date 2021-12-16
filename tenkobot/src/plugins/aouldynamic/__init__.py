import nonebot
from bilibili_api import user, sync
from nonebot import on_command, on_message, on_keyword, require, on_notice
from nonebot.adapters.cqhttp import Bot, Event, Message, MessageSegment, escape
from nonebot.typing import T_State
from nonebot import require

scheduler = require("nonebot_plugin_apscheduler").scheduler

u = user.User(703007996)


async def get_dynamic(dynamics):
    for dynamic in dynamics:
        if not ('origin' in dynamic['card']):
            try:
                if '日程表' in dynamic['card']['item']['description']:
                    return dynamic
            except KeyError:
                continue
    return 0


async def main():
    offset = 0
    while True:
        # 获取该页动态
        page = await u.get_dynamics(offset)
        if 'cards' in page:
            dynamics = page['cards']
            target = await get_dynamic(dynamics)
            if target != 0:
                return target

        if page['has_more'] != 1:
            # 如果没有更多动态，跳出循环
            break

        # 设置 offset，用于下一轮循环
        offset = page['next_offset']


daily = on_command("rcb", aliases={"日程表"}, priority=1, block=True)


@daily.handle()
async def dynamic_handle(bot: Bot, event: Event, state: T_State):
    m = event.get_message()
    m.clear()
    dynamic = await main()
    m.append(dynamic['card']['item']['description'])
    src = []
    for i in dynamic['card']['item']['pictures']:
        src.append(i['img_src'])
    for i in src:
        m.append(f'[CQ:image,file={i}]')
    await daily.finish(m)


async def get_bot():
    bots = nonebot.get_bots()
    bot = list(bots.values())[0]
    return bot


# @scheduler.scheduled_job('cron', second='*/5')
@scheduler.scheduled_job('cron', hour='7', minute='30')
async def go():
    bot = await get_bot()
    m = Message()
    dynamic = await main()
    m.append(dynamic['card']['item']['description'])
    src = []
    for i in dynamic['card']['item']['pictures']:
        src.append(i['img_src'])
    for i in src:
        m.append(f'[CQ:image,file={i}]')
    await bot.send_group_msg(group_id=795179664, message=m)

# async def run_as_command(hour, minute):
#     scheduler.add_job(go, "cron", hour=hour, minute=minute)
#
#
# test = on_command("test", priority=1, block=True)
#
#
# @test.handle()
# async def test_handle(bot: Bot, event: Event, state: T_State):
#     words = str(event.get_message()).strip().split(':')
#     print(words)
#     await run_as_command(words[0], words[1])
