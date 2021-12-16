import random
from bilibili_api import user, video
from nonebot import on_command, on_message, on_keyword, require, on_notice
from nonebot.adapters.cqhttp import Bot, Event, Message, MessageSegment, escape
from nonebot.rule import to_me
from nonebot.typing import T_State
import time
import aiohttp
import nonebot

# # scheduler = require('nonebot_plugin_apscheduler').scheduler
#
# async def get_bot():
#     bots = nonebot.get_bots()
#     bot = list(bots.values())[0]
#     return bot
#
#
# #
# #
# # @scheduler.scheduled_job('cron', second='*/2')
# # async def run_every_2_hour():
# #     bot = await get_bot()
# #     await bot.send_group_msg(group_id=611153874, message="test")


repeat = on_message(block=True, priority=50)


@repeat.handle()
async def repeat_handle(bot: Bot, event: Event):
    if 0.5 <= random.random() < 0.51:
        await repeat.finish(event.get_message())
    else:
        await repeat.finish()


water = on_notice(priority=1, block=True, rule=to_me())


@water.handle()
async def water_handle(bot: Bot, event: Event, state: T_State):
    if event.get_event_name() == 'notice.notify.poke':
        await water.finish("🐳")
