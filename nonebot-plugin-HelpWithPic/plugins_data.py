from pathlib import Path
#from util.config import *
#from nonebot import get_driver
import os
import json
from loguru import logger
#driver = get_driver()
# 插件数据代理

path_name="plugins_data"
dir_path = Path(Path(path_name)).absolute()

if dir_path.is_dir():
    logger.opt(colors=True).debug(f"\033[1;36;43m[plugin_data]\033[0m根目录正常-\<{path_name}\>")
else:
    #os.mkdir(path_name)
    os.mkdir(dir_path)
    logger.opt(colors=True).debug(f"\033[1;36;43m[plugin_data]\033[0m初始化根目录\<{path_name}\>")

def initdata(
    conf_name,
    bashdata:dict={"status":1}
):
    conf_path = Path(dir_path / conf_name).absolute()
    config_init(conf_path,conf_name,"plugin_data",bashdata)
    return True

def rdata(
    conf_name
):
    conf_path = Path(dir_path / conf_name).absolute()
    with open(conf_path, "r", encoding="utf-8") as f:
        data = json.loads(f.read())
    return data

def wdata(
    conf_name:str,
    data:dict
):
    conf_path = Path(dir_path / conf_name).absolute()
    with open(conf_path, "w", encoding="utf-8") as f:
        f.write(json.dumps(data, indent=4,ensure_ascii=False))
    return True

def config_init(
    _path_ ,
    conf_name:str ,
    module_name:str="None" ,
    data:dict={"status":1}
):
    if _path_.is_file():
        logger.opt(colors=True).debug(f"\033[1;36;43m[util]\033[0m>>><W>{module_name}</>>>>{conf_name}-OK!")
    else:
        logger.opt(colors=True).debug(f"\033[1;36;43m[util]\033[0m>>><W>{module_name}</>>>>Create-{conf_name}!")
        with open(_path_, "w", encoding="utf-8") as f:
            f.write(json.dumps(data, indent=4))
            f.close()

#本插件由 cubstaryow 编写