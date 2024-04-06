
from .jsondata import addHWP, delHWP, format_data
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from nonebot import on_command , on_regex
from .draw import get_help_pic
from nonebot.matcher import Matcher
from .config import config
from nonebot.adapters.onebot.v11 import (
    Bot, MessageEvent, MessageSegment, GroupMessageEvent, Message
)
import asyncio
from nonebot_plugin_saa import Image, Text, MessageFactory

# 你需要自己设计一个命令权限检查器！
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
        #matcher: Matcher,
        data: list = CommandArg()
):
    cdata = str(data[0])
    cdatal = cdata.split("\n")
    if len(cdatal) < 1:
        msg = "[HWP-E]缺失重要参数!"
    else:
        if len(cdatal) < 2:
            cdatal[1] = ""
        if len(cdatal) < 3:
            cdatal[2] = "unknow"
        ret = addHWP(
            command=cdatal[0].strip(),
            text=cdatal[1].strip(),
            perm=cdatal[2].strip()
        )
        if ret:
            msg = "[HWP-I]词条已添加"
    msg_builder = MessageFactory([
        Text(msg)
    ])
    await msg_builder.send()

@del_cmd.handle()
async def HWP_dc(
    #matcher: Matcher,
    data: list = CommandArg()
        
):
    command = str(data[1]).strip()
    ret = delHWP(
        command=command
    )
    if ret != "NotFound":
       msg = f"[HWP-I]词条已删除\n>{command}"
    else:
        msg = f"[HWP-E]词条未找到"
    msg_builder = MessageFactory([
        Text(msg)
    ])
    await msg_builder.send()


@helppic.handle()
async def HWP_mb(
        bot: Bot,
        event: MessageEvent,
        #matcher: Matcher,
):
    pic = None
    # try :
    #    pic = await extract_msg_pic(bot, event)
    # except Exception:
    #    logger.exception("获取消息中附带图片失败，回退到默认行为")
    user = await bot.get_stranger_info(user_id=event.self_id, no_cache=False)
    data = format_data()
    try:

        ret = await get_help_pic(data=data,user=user,bg_arg=pic)
        msg_builder = MessageFactory([
            Image(ret)
        ])
    except Exception:
        msg_builder = MessageFactory([
            Text("[HWP-E]出错了,请查看控制台")])
    await msg_builder.send()
    await helppic.finish()

#本插件由 cubstaryow 编写