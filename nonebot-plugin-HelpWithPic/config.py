from typing import List, Literal, Optional, Set, Tuple

from nonebot import get_driver
from pydantic import BaseModel

class config_hwp(BaseModel):
    superusers: Set[str] = set()
    hwp_font: Optional[str] = None
    hwp_custom_bg: List[str] = []
    #ps_blur_radius: int = 4
    #ps_bg_color: Tuple[int, int, int, int] = (255, 255, 255, 150)
    #ps_mask_color: Tuple[int, int, int, int] = (255, 255, 255, 125)
    version: str = "Unknow"
    hwp_commandstart :str = "#"
    hwp_nickname:str ="幼龙云V4的帮助文档"
    hwp_text:str =  "你想要的,我们都没有(不是\n不知道写啥了"
    hwp_version:str="HelpWithPic-Beta1.2"

config: config_hwp = config_hwp.parse_obj(get_driver().config.dict())
#本插件由 cubstaryow 编写