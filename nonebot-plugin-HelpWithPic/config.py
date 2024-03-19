from typing import List, Literal, Optional, Set, Tuple

from nonebot import get_driver
from pydantic import BaseModel

class config_HWP(BaseModel):
    superusers: Set[str] = set()
    ps_font: Optional[str] = None
    ps_custom_bg: List[str] = []
    version: str = "Unknow"
    HWP_commandstart :str = "#"
    HWP_nickname:str ="本bot的帮助文档"
    HWP_text:str = "你想要的,我们都没有(不是\n这是描述"
    plugin_version:str="HelpWithPic-Beta1.0"

config: config_HWP = config_HWP.parse_obj(get_driver().config.dict())

#本插件由 cubstaryow 编写