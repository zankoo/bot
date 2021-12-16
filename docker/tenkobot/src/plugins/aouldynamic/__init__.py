from bilibili_api import user, sync
from nonebot import on_command, on_message, on_keyword, require, on_notice
from nonebot.adapters.cqhttp import Bot, Event, Message, MessageSegment, escape
from nonebot.typing import T_State

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
