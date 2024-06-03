
from .jsondata import addHWP, delHWP, format_data
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from nonebot import on_command , on_regex
from nonebot.matcher import Matcher
from .draw import get_help_pic
from .config import config
from nonebot.adapters.onebot.v11 import (
    Bot, MessageEvent , MessageSegment
)
from nonebot.adapters.onebot.v11 import (
    GROUP_ADMIN , GROUP_OWNER
)
import asyncio

commandstart = config.hwp_commandstart

add_cmd = on_command(
    commandstart+"helpadd",
    aliases={ commandstart+"菜单添加" } ,
    permission=SUPERUSER, priority=20
)
del_cmd = on_command(
    commandstart+"helpdel",
    aliases={ commandstart+"菜单删除"} ,
    permission=SUPERUSER, priority=20
)
helppic = on_regex(
    rf"^{commandstart}(help|帮助)$",
    priority=19
)


@add_cmd.handle()
async def HWP_rc(
        matcher: Matcher,
        data: list = CommandArg()
):  
    try:
        cdata = str(data[0])
        cdatal = cdata.split(config.hwp_addseparator)
        if len(cdatal) < 1:
            msg = "[HWP-E]缺失重要参数!"
        else:
            if len(cdatal) < 2:
                cdatal.append("")
            if len(cdatal) < 3:
                cdatal.append("unknow")
            ret = addHWP(
                command=cdatal[0].strip(),
                text=cdatal[1].strip(),
                perm=cdatal[2].strip()
            )
            if ret:
                msg = "[HWP-I]词条已添加"
        await matcher.send(msg)
    except Exception as e:
        msg = f"[HWP-E]出错了\n{e}"
        await matcher.send(msg)
        raise e
    

@del_cmd.handle()
async def HWP_dc(
    matcher: Matcher,
    data: list = CommandArg()
        
):
    try:
        command = str(data[0]).strip()
        ret = delHWP(
            command=command
        )
        if ret != "NotFound":
           msg = f"[HWP-I]词条已删除\n>{command}"
        else:
            msg = f"[HWP-E]词条未找到"
        await matcher.send(msg)
    except Exception as e:
        msg = f"[HWP-E]出错了\n{e}"
        await matcher.send(msg)
        raise e


@helppic.handle()
async def HWP_mb(
        bot: Bot,
        event: MessageEvent,
        matcher: Matcher
):
    pic = None
    # try :
    #    pic = await extract_msg_pic(bot, event)
    # except Exception:
    #    logger.exception("获取消息中附带图片失败，回退到默认行为")
    try:
        user = await bot.get_stranger_info(user_id=event.self_id, no_cache=False)
        data = format_data( await checkperm(bot=bot,event=event))
        ret = await get_help_pic(data=data,user=user,bg_arg=pic)
        msg = MessageSegment.image(ret)
        await matcher.send(msg)
    except Exception as e:
        msg = f"[HWP-E]出错了\n{e}"
        await matcher.send(msg)
        raise e

    

async def checkperm(bot:Bot,event: MessageEvent):
    if await SUPERUSER(bot,event):
        return 'root'
    if await GROUP_OWNER(bot,event):
        return 'admin'
    if await GROUP_ADMIN(bot,event):
        return 'admin'
    return 'user'


#本插件由 cubstaryow 编写