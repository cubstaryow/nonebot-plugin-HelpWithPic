from typing import List,Optional

from nonebot import get_driver
from pydantic import BaseModel

class config_hwp(BaseModel):
    #superusers: Set[str] = set() 以后可能会内置权限检查器，现在用不到
    hwp_font: Optional[str] = None
    hwp_custom_bg: List[str] = []
    version: str = "Unknow"
    hwp_commandstart :str = "#"
    hwp_nickname:str ="本BOT的帮助文档"
    hwp_text:str =  "你想要的,我们都没有(不是\n不知道写啥了"
    hwp_version:str="HelpWithPic-Beta1.6"
    cubplugin_datadir:str=""
    hwp_addseparator:str="\n"

config: config_hwp = config_hwp.parse_obj(get_driver().config.dict())
#本插件由 cubstaryow 编写