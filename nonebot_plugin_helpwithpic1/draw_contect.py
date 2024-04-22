from io import BytesIO
import aiohttp
import anyio
from PIL import Image


async def get_qq_avatar(qq) -> bytes:
    return await api_get_img(f"https://q2.qlogo.cn/headimg_dl?dst_uin={qq}&spec=640")

async def async_open_img(fp, *args, **kwargs) -> Image.Image:
    async with (await anyio.open_file(fp, "rb")) as f:
        p = BytesIO(await f.read())
    return Image.open(p, *args, **kwargs)

        
apiurl="https://cn.bing.com"

async def bing_dayimg(n : int = 1 , idx : int = 0):
    api = apiurl + f"/HPImageArchive.aspx?n={n}&format=js&idx={idx}"
    data = await api_get(api)
    imgurl = apiurl + str(data.get("images",[])[0].get("url",""))
    return imgurl

async def api_get(url: str ,headers:dict={},cookies:dict={}):
    """异步api调用,get类型
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url,headers=headers,cookies=cookies) as response:
            return await response.json(content_type=None)

async def api_get_img(url: str ,headers:dict={},cookies:dict={}):
    """异步api调用,get类型 获取图片
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url,headers=headers,cookies=cookies) as response:
            return await response.content.read()