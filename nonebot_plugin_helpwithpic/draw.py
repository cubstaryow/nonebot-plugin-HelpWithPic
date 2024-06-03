import asyncio
import math
import platform
import time
from typing import Optional, Union
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from loguru import logger
from pil_utils import BuildImage
from pil_utils.fonts import get_proper_font
import random
from .draw_contect import *
from .config import config

GRAY_BG_COLOR: str = "#aaaaaaaa"
WHITE_BG_COLOR = (255, 255, 255, 150)
WHITE_MASK_COLOR = (255, 255, 255, 125)

FONT_PATH =  config.hwp_font or str(get_proper_font("国").path.resolve())
#"./util/resource/font/Rajdhani-zihun-Medium.ttf" or

nick = config.hwp_nickname
text =  config.hwp_text
cs = config.hwp_commandstart
hwp_version = config.hwp_version

version = config.version

def get_font(size: int):
    return ImageFont.truetype(FONT_PATH, size)

font_size_add = 0   #5
font_20 = get_font(20 + font_size_add)
font_30 = get_font(30 + font_size_add)
font_40 = get_font(40 + font_size_add)
font_45 = get_font(45 + font_size_add)

font_footer = get_font( 32 )



async def draw_header(user) -> Image.Image:
    #avatar = await async_open_img(url[8:])
    avatar = await get_qq_avatar(user.get("user_id"))
    avatar = Image.open(BytesIO(avatar))
    bg = Image.new("RGBA", (1900,260),"#ffffff00")
    
    bg_main = Image.new("RGBA", (865,260), WHITE_BG_COLOR)
    bg_draw = ImageDraw.Draw(bg_main)
    
    rectangle = Image.new("RGBA", (800, 220), "#ffd05080")
    ImageDraw.Draw(rectangle).rectangle((0,0,800,220), fill=None, outline='red', width=5)
    # 圆形遮罩
    rectangle_mask = Image.new("RGBA", (800, 220), "#ffffff00")
    ImageDraw.Draw(rectangle_mask).polygon([(0,0),(800,0),(0,1200)],fill='black', outline=None)
    
    circle_mask = Image.new("RGBA", (190, 190), "#ffffff00")
    ImageDraw.Draw(circle_mask).ellipse((0, 0, 190, 190), fill="black")

    # 利用遮罩裁剪圆形图片
    avatar = avatar.convert("RGBA").resize((190, 190))
    bg_main.paste(rectangle, (20, 20),rectangle_mask)
    bg_main.paste(avatar, (35, 35), circle_mask)

    # 标题
    # bg_draw.text((300, 140), nick, "black", font_80, "ld")
    BuildImage(bg_main).draw_text(
        (240, 35, 775, 110),
        nick,
        max_fontsize=60,
        halign="left",
        valign="bottom",
        fontname=FONT_PATH,
    )
    # 详细信息
    BuildImage(bg_main).draw_text(
        (240, 110, 775, 220),
        text,
        max_fontsize=40,
        halign="left",
        valign="top",
        fontname=FONT_PATH,
    )

    # 标题与详细信息的分隔线
    bg_draw.line((240, 110, 750, 110), GRAY_BG_COLOR, 3)
    
    bg_mask = Image.new("RGBA", (865, 260), "#ffffff00")
    ImageDraw.Draw(bg_mask).polygon([(0,0),(865,0),(0,1265)],fill='black')
    bg.paste(bg_main, (0, 0), bg_mask)

    bg_help = Image.new("RGBA", (865,260), WHITE_BG_COLOR)
    bg_draw = ImageDraw.Draw(bg_help)
    aaa = await make_command_card(
        f"{cs}help / {cs}帮助","获取本帮助页",300
        )
    bbb = await make_command_card(
        f"{cs}helpadd [命令]</>[描述]</>[触发权限]","为本帮助页添加一条命令,</>默认为换行",750,perm="admin"
        )
    ccc = await make_command_card(
        f"{cs}helpdel [命令]","删除一条命令",400,perm="admin"
        )
    unkown = await make_command_card("unkown","",250 ,"unkown","center")
    user = await make_command_card("user","",250 ,"user","center")
    admin = await make_command_card("admin","",250 ,"admin","center")
    root = await make_command_card("root","权限颜色示例",250 ,"root","center")
    bg.paste(aaa , (860, 20) , aaa)
    bg.paste(bbb , (800, 140) , bbb)
    bg.paste(ccc , (1150, 20) , ccc)
    bg.paste(unkown , (1600, 20) , unkown)
    bg.paste(user , (1600, 60) , user)
    bg.paste(admin , (1600, 100) , admin)
    bg.paste(root , (1600, 140) , root)
    return bg

async def command_pic(data):
    lenc = len(data)
    lenbg = math.ceil(lenc/3.0)
    bg = Image.new("RGBA", (1900,lenbg*140),"#ffffff00")
    sidel ,sidew = 33 ,20
    for temp in data:
        aaa = await make_command_card(
            temp[0],temp[1],600,temp[2]
        )
        bg.paste(aaa , (sidel, sidew) , aaa)
        sidel +=600
        if sidel > 1800:
            sidel = 33
            sidew +=140
    return bg

from .basedata import permcolor

async def make_command_card(
    text:str , 
    text2:str="",
    long:int=600,
    perm:str="user",
    chalign:str = "center"
):
    main_card  = Image.new("RGBA", (long,100), "#ffffff00")
    color = permcolor.get(perm,["#c8d6e5c0","#8395a7"])
    
    command_card = Image.new("RGBA", (long,100), color[0])
    card_draw = ImageDraw.Draw(command_card)
    card_draw.line((0, 60, long-20, 60), GRAY_BG_COLOR, 3)
    ImageDraw.Draw(command_card).polygon([(0,0),(70,0),(0,140)],fill=color[1])
    BuildImage(command_card).draw_text(
        (60, 0, long*0.95, 60),
        text,
        max_fontsize=55,
        halign=chalign,
        valign="bottom",
        fontname=FONT_PATH,
    )
    BuildImage(command_card).draw_text(
        (40, 60, long*0.9, 100),
        text2,
        max_fontsize=35,
        halign="left",
        valign="bottom",
        fontname=FONT_PATH,
    )
    
    bg_mask = Image.new("RGBA", (long, 100), "#ffffff00")
    ImageDraw.Draw(bg_mask).polygon([(long*0.5,0),(long,0),(long*0.5,long)],fill='black')
    ImageDraw.Draw(bg_mask).polygon([(0,100),(long*0.5,100),(long*0.5,100-long)],fill='black')
    
    main_card.paste(command_card,(0,0),bg_mask)
    return main_card



async def get_bg(pic: Optional[Union[bytes, Image.Image]] = None) -> Image.Image:
    if len(config.hwp_custom_bg) >0:
        try:
            url=random.choice(config.hwp_custom_bg)
            if url.startswith("file:///"):
                return await async_open_img(url[8:])
            return Image.open(await api_get_img(url))
        except Exception:
            logger.exception("下载/打开自定义背景图失败")
            
    try:
        return Image.open(await api_get_img(await bing_dayimg()))
    except:
        logger.exception("获取bing背景图失败")

async def draw_footer(img: Image.Image, time_str: str):
    draw = ImageDraw.Draw(img)
    w, h = img.size
    padding = 15
    
    draw.text(
        (w / 2, h - padding),
        (
            f"{hwp_version} | "
            f"{version} | "
            f"{platform.python_implementation()} {platform.python_version()} | "
            f"{time_str}"
        ),
        "darkslategray",
        font_footer,
        "ms",
    )

async def get_help_pic(data: dict,user :dict,bg_arg: Optional[bytes] = None) -> bytes:
    img_w = 2000
    img_h = 50  # 这里是上边距，留给下面代码统计图片高度
    now_time = time.strftime("%Y-%m-%d %H:%M:%S")

    # 获取背景及各模块图片
    ret = await asyncio.gather(
        get_bg(),
        draw_header(user),
        command_pic(data)

    )

    bg = ret[0]
    ret = ret[1:]

    # 统计图片高度
    for p in ret:
        if p:
            img_h += p.size[1] + 50

    # 居中裁剪背景
    bg = bg.convert("RGBA")
    bg_w, bg_h = bg.size

    scale = img_w / bg_w
    scaled_h = int(bg_h * scale)

    if scaled_h < img_h:  # 缩放后图片不够高（横屏图）
        # 重算缩放比
        scale = img_h / bg_h
        bg_w = int(bg_w * scale)

        crop_l = round((bg_w / 2) - (img_w / 2))
        bg = bg.resize((bg_w, img_h)).crop((crop_l, 0, crop_l + img_w, img_h))
    else:
        bg_h = scaled_h

        crop_t = round((bg_h / 2) - (img_h / 2))
        bg = bg.resize((img_w, bg_h)).crop((0, crop_t, img_w, crop_t + img_h))

    # 背景高斯模糊
    bg = bg.filter(ImageFilter.GaussianBlur(radius=4))

    # 贴一层白色遮罩
    bg.paste(i := Image.new("RGBA", (img_w, img_h), WHITE_MASK_COLOR), mask=i)

    # 将各模块贴上背景
    h_pos = 50
    for p in ret:
        if p:
            bg.paste(p, (50, h_pos), p)
            h_pos += p.size[1] + 50

    # 写footer
    await draw_footer(bg, now_time)

    # 尝试解决黑底白底颜色不同问题
    bg = bg.convert("RGB")

    bio = BytesIO()
    bg.save(bio, "jpeg")
    return bio.getvalue()
