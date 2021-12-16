from bilibili_api import user, sync

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
    dynamics = []
    while True:
        # 获取该页动态
        page = await u.get_dynamics(offset)
        if 'cards' in page:
            dynamics = page['cards']
            target = await get_dynamic(dynamics)
            if target != 0:
                print(target)
                return

        if page['has_more'] != 1:
            # 如果没有更多动态，跳出循环
            break

        # 设置 offset，用于下一轮循环
        offset = page['next_offset']


if __name__ == '__main__':
    sync(main())
