from io import BytesIO
from typing import List, Literal, Optional, cast, overload

import anyio
from httpx import AsyncClient
from nonebot import logger
from nonebot.internal.adapter import Bot , Event
from PIL import Image

try:
    from nonebot.adapters.onebot.v11 import MessageEvent as OBV11MessageEvent
except ImportError:
    OBV11MessageEvent = None

@overload
async def async_request(
    url: str,
    *args,
    is_text: Literal[False] = False,
    proxy: Optional[str] = None,
    **kwargs,
) -> bytes:
    ...


@overload
async def async_request(
    url: str,
    *args,
    is_text: Literal[True] = True,
    proxy: Optional[str] = None,
    **kwargs,
) -> str:
    ...


async def async_request(url: str, *args, is_text=False, proxy=None, **kwargs):
    async with AsyncClient(
        proxies=proxy,
        follow_redirects=True,
        timeout=10,
    ) as cli:
        res = await cli.get(url, *args, **kwargs)
        return res.text if is_text else res.content

async def get_qq_avatar(qq) -> bytes:
    return await async_request(f"https://q2.qlogo.cn/headimg_dl?dst_uin={qq}&spec=640")


async def async_open_img(fp, *args, **kwargs) -> Image.Image:
    async with (await anyio.open_file(fp, "rb")) as f:
        p = BytesIO(await f.read())
    return Image.open(p, *args, **kwargs)

async def extract_msg_pic(bot: Bot, event: Event) -> Optional[bytes]:
    if OBV11MessageEvent and isinstance(event, OBV11MessageEvent):
        if (event.reply and (img := event.reply.message["image"])) or (
            img := event.message["image"]
        ):
            url = img[0].data["url"]
            return await async_request(url)